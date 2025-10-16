from django.core.management.base import BaseCommand
from subscriptions.models import SubscriptionPlan
from tokens.models import TokenLimit
from core.enums import PeriodicChoices


class Command(BaseCommand):
    help = "Initialize subscription plans with token limits"

    def handle(self, *args, **options):
        plans_data = [
            {
                "name": "Free",
                "description": "Perfect for getting started with basic features",
                "price": 0.00,
                "is_free": True,
                "token_limits": {
                    PeriodicChoices.DAY: 2000,
                    PeriodicChoices.WEEK: 10000,
                    PeriodicChoices.MONTH: 100000,
                },
            },
            {
                "name": "Basic",
                "description": "Great for individuals and small teams",
                "price": 9.99,
                "is_free": False,
                "token_limits": {
                    PeriodicChoices.DAY: 5000,
                    PeriodicChoices.WEEK: 20000,
                    PeriodicChoices.MONTH: 200000,
                },
            },
            {
                "name": "Pro",
                "description": "For professionals who need advanced features",
                "price": 29.99,
                "is_free": False,
                "token_limits": {
                    PeriodicChoices.DAY: 10000,
                    PeriodicChoices.WEEK: 50000,
                    PeriodicChoices.MONTH: 300000,
                },
            },
            {
                "name": "Enterprise",
                "description": "Custom solutions for large organizations",
                "price": 99.99,
                "is_free": False,
                "token_limits": {
                    PeriodicChoices.DAY: 50000,
                    PeriodicChoices.WEEK: 250000,
                    PeriodicChoices.MONTH: 1000000,
                },
            },
        ]

        self.stdout.write("\nCreating subscription plans...")
        for plan_data in plans_data:
            token_limits = plan_data.pop("token_limits")

            plan, created = SubscriptionPlan.objects.get_or_create(
                name=plan_data["name"], defaults=plan_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nCreated: {plan.name} ({plan.price}/{plan.get_interval_display()})"
                    )
                )

                for period, limit in token_limits.items():
                    TokenLimit.objects.get_or_create(
                        subscription_plan=plan, period=period, defaults={"limit": limit}
                    )
                    self.stdout.write(f"  • {period.label}: {limit:,} tokens")
            else:
                self.stdout.write(
                    self.style.WARNING(f"- Plan {plan.name} already exists")
                )

        self.stdout.write(self.style.SUCCESS("\nSuccessfully initialized!"))
