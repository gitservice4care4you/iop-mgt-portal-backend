from django.core.management.base import BaseCommand
from country.models import Country


class Command(BaseCommand):
    help = 'Seeds MENA (Middle East and North Africa) region countries with their codes'

    def handle(self, *args, **options):
        # List of MENA countries with their ISO codes
        mena_countries = [
            {"name": "Algeria", "code": "DZ"},
            {"name": "Bahrain", "code": "BH"},
            {"name": "Egypt", "code": "EG"},
            {"name": "Iran", "code": "IR"},
            {"name": "Iraq", "code": "IQ"},
            {"name": "Israel", "code": "IL"},
            {"name": "Jordan", "code": "JO"},
            {"name": "Kuwait", "code": "KW"},
            {"name": "Lebanon", "code": "LB"},
            {"name": "Libya", "code": "LY"},
            {"name": "Morocco", "code": "MA"},
            {"name": "Oman", "code": "OM"},
            {"name": "Palestine", "code": "PS"},
            {"name": "Qatar", "code": "QA"},
            {"name": "Saudi Arabia", "code": "SA"},
            {"name": "Syria", "code": "SY"},
            {"name": "Tunisia", "code": "TN"},
            {"name": "United Arab Emirates", "code": "AE"},
            {"name": "Yemen", "code": "YE"},
        ]
        
        countries_created = 0
        countries_existing = 0

        for country_data in mena_countries:
            country, created = Country.objects.get_or_create(
                code=country_data["code"],
                defaults={"name": country_data["name"]}
            )
            
            if created:
                countries_created += 1
                self.stdout.write(self.style.SUCCESS(f'Created country: {country.name} ({country.code})'))
            else:
                countries_existing += 1
                self.stdout.write(self.style.WARNING(f'Country {country.name} ({country.code}) already exists'))
        
        self.stdout.write(self.style.SUCCESS(f'Countries created: {countries_created}'))
        self.stdout.write(self.style.SUCCESS(f'Countries already existing: {countries_existing}')) 