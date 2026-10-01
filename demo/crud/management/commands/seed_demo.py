"""Populate the demo database with a small, realistic relational dataset.

Deterministic and idempotent — running it repeatedly yields the same data
(it clears the crud tables first). It also (re)sets the public demo account
from ``settings.DEMO_ACCOUNT`` (default ``admin`` / ``adminpass``): a **staff,
non-superuser** account that can view everything in the admin and add, change
and delete the sample data, but cannot touch users, groups or permissions. An
existing account with that username — including the superuser that seed_demo
created before 0.3.1 — is demoted and its password and permissions reset.

The live demo runs this nightly (systemd timer, 04:00 UTC) to reset the data
and the account.

    python manage.py seed_demo
    python manage.py seed_demo --no-demo-user   # data only
"""

import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from crud.models import Company, Contact, Project, Tag, Task

COMPANIES = [
    ("Acme Technology", "tech", "https://acme.example"),
    ("Globex Finance", "finance", "https://globex.example"),
    ("Initech Software", "tech", "https://initech.example"),
    ("Umbrella Health", "health", "https://umbrella.example"),
    ("Wayne Media", "media", "https://wayne.example"),
    ("Stark Retail", "retail", "https://stark.example"),
]

TAGS = [
    ("Frontend", "primary"), ("Backend", "info"), ("Design", "success"),
    ("Urgent", "danger"), ("Research", "warning"), ("Infra", "secondary"),
]

CONTACT_NAMES = [
    "Ada Lovelace", "Grace Hopper", "Alan Turing", "Linus Torvalds",
    "Guido van Rossum", "Margaret Hamilton", "Ken Thompson", "Barbara Liskov",
    "Donald Knuth", "Tim Berners-Lee", "Dennis Ritchie", "Radia Perlman",
    "Brian Kernighan", "Anita Borg", "Edsger Dijkstra", "Katherine Johnson",
    "James Gosling", "Hedy Lamarr", "Bjarne Stroustrup", "Adele Goldberg",
    "John McCarthy", "Frances Allen", "Vint Cerf", "Joan Clarke",
]
ROLES = ["admin", "editor", "viewer"]
CONTACT_STATUS = ["active", "pending", "disabled"]

PROJECTS = [
    ("Website Redesign", "active"), ("Mobile App v2", "planning"),
    ("Data Warehouse", "active"), ("Payment Gateway", "on_hold"),
    ("Brand Refresh", "completed"), ("Customer Portal", "active"),
    ("Analytics Pipeline", "planning"), ("Security Audit", "active"),
    ("Inventory System", "on_hold"), ("Marketing Campaign", "completed"),
]

TASK_TITLES = [
    "Kick-off meeting", "Requirements gathering", "Design mockups",
    "Implementation", "Code review", "QA testing", "Deployment",
    "Documentation", "Stakeholder demo", "Retrospective",
]
TASK_STATUS_CYCLE = ["done", "done", "in_progress", "todo"]

DEMO_GROUP = "Demo visitors"
# Apps whose data the demo account may add/change/delete (reset nightly).
# Everything else registered in the admin — users, groups, e-mail addresses —
# is view-only, so the shared account can never grant itself (or anyone)
# more rights or lock other visitors out.
DEMO_WRITE_APPS = {"crud"}


def demo_account_settings():
    return {
        "username": "admin",
        "password": "adminpass",
        "email": "admin@example.com",
        **getattr(settings, "DEMO_ACCOUNT", {}),
    }


def demo_permissions():
    """View on every model in the admin; add/change/delete on the demo data."""
    perms = []
    for model in sorted(admin.site._registry, key=lambda m: m._meta.label):
        opts = model._meta
        actions = ["view"]
        if opts.app_label in DEMO_WRITE_APPS:
            actions += ["add", "change", "delete"]
        content_type = ContentType.objects.get_for_model(model)
        perms += Permission.objects.filter(
            content_type=content_type,
            codename__in=[f"{action}_{opts.model_name}" for action in actions],
        )
    return perms


def ensure_demo_account():
    """Create or reset the public demo account (staff, never superuser)."""
    cfg = demo_account_settings()
    User = get_user_model()
    user, created = User.objects.get_or_create(username=cfg["username"])
    user.email = cfg["email"]
    user.is_active = True
    user.is_staff = True
    user.is_superuser = False
    if not user.check_password(cfg["password"]):
        # Only when it differs: re-hashing would sign out every visitor.
        user.set_password(cfg["password"])
    user.save()
    group, _ = Group.objects.get_or_create(name=DEMO_GROUP)
    group.permissions.set(demo_permissions())
    user.groups.set([group])
    user.user_permissions.clear()
    return user, created


class Command(BaseCommand):
    help = "Seed the demo database with a relational sample dataset (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-demo-user", action="store_true",
            help="Do not create/reset the demo account (settings.DEMO_ACCOUNT).",
        )
        parser.add_argument(
            "--no-superuser", action="store_true",
            help="Deprecated alias of --no-demo-user (the demo account is no longer a superuser).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        today = datetime.date.today()

        # Clean slate (child → parent order).
        Task.objects.all().delete()
        Project.objects.all().delete()
        Contact.objects.all().delete()
        Tag.objects.all().delete()
        Company.objects.all().delete()

        companies = [
            Company.objects.create(name=n, industry=ind, website=url)
            for n, ind, url in COMPANIES
        ]
        tags = [Tag.objects.create(name=n, color=c) for n, c in TAGS]

        contacts = []
        for i, name in enumerate(CONTACT_NAMES):
            first = name.split()[0].lower()
            contacts.append(Contact.objects.create(
                name=name,
                email=f"{first}@{companies[i % len(companies)].name.split()[0].lower()}.example",
                role=ROLES[i % len(ROLES)],
                status=CONTACT_STATUS[i % len(CONTACT_STATUS)],
                company=companies[i % len(companies)],
            ))

        task_total = 0
        for i, (pname, status) in enumerate(PROJECTS):
            # Spread starts across ~5 months so the dashboard chart has a curve.
            start = today - datetime.timedelta(days=150 - i * 15)
            project = Project.objects.create(
                name=pname,
                company=companies[i % len(companies)],
                status=status,
                budget=Decimal(25000 + i * 7500),
                start_date=start,
                due_date=start + datetime.timedelta(days=90),
                lead=contacts[i % len(contacts)],
            )
            team = [contacts[(i + k) % len(contacts)] for k in range(4)]
            project.team.set(team)
            project.tags.set([tags[i % len(tags)], tags[(i + 2) % len(tags)]])

            for k in range(4):
                title = TASK_TITLES[(i + k) % len(TASK_TITLES)]
                Task.objects.create(
                    project=project,
                    title=title,
                    status=TASK_STATUS_CYCLE[k % len(TASK_STATUS_CYCLE)],
                    assignee=team[k % len(team)],
                    due_date=start + datetime.timedelta(days=15 * (k + 1)),
                    order=k,
                )
                task_total += 1

        verbose = int(options.get("verbosity", 1))
        if not (options["no_demo_user"] or options["no_superuser"]):
            user, created = ensure_demo_account()
            if verbose:
                self.stdout.write(self.style.WARNING(
                    f"{'Created' if created else 'Reset'} demo account  "
                    f"{user.get_username()} / {demo_account_settings()['password']}  "
                    "(staff, not superuser)"
                ))

        if verbose:
            self.stdout.write(self.style.SUCCESS(
                f"Seeded {len(companies)} companies, {len(tags)} tags, {len(contacts)} contacts, "
                f"{len(PROJECTS)} projects, {task_total} tasks."
            ))
