from django.core.management.base import BaseCommand
from role.models import Role
from role.enums import RoleEnum


class Command(BaseCommand):
    help = 'Seeds the default roles into the database'

    def handle(self, *args, **options):
        roles_created = 0
        roles_existing = 0

        for role_choice in RoleEnum.choices:
            role_name, role_label = role_choice
            role, created = Role.objects.get_or_create(
                name=role_name,
                defaults={
                    'description': f'Default role for {role_label}'
                }
            )
            
            if created:
                roles_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created role: {role_name}'))
            else:
                roles_existing += 1
                self.stdout.write(self.style.WARNING(f'Role {role_name} already exists'))
        
        self.stdout.write(self.style.SUCCESS(f'Roles created: {roles_created}'))
        self.stdout.write(self.style.SUCCESS(f'Roles already existing: {roles_existing}')) 