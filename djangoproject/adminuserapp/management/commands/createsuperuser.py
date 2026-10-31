from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.exceptions import ValidationError
from django.core.management.base import CommandError

class Command(BaseCommand):
    help = 'Creates a superuser with a custom user model'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--nickname',
            dest='nickname',
            default=None,
            help='Specifies the nickname for the superuser.',
        )

    def handle(self, *args, **options):
        options['username'] = options.get('username') or input('Username: ')
        options['email'] = options.get('email') or input('Email address: ')
        options['nickname'] = options.get('nickname') or input('Nickname: ')

        # Call the original handle method from BaseCommand
        try:
            super().handle(*args, **options)
        except ValidationError as e:
            raise CommandError('; '.join(e.messages))