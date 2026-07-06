import os
import sys
import django
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db import IntegrityError
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crowdfunding.settings')
django.setup()

from accounts.models import User
from projects.models import Project


class Command(BaseCommand):
    help = 'Crowdfunding Console Application'
    current_user = None

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('==== Crowdfunding Console Application ===='))
        while True:
            if not self.current_user:
                self.show_main_menu()
            else:
                self.show_user_menu()

    def show_main_menu(self):
        self.stdout.write('\nMain Menu:')
        self.stdout.write('1. Register')
        self.stdout.write('2. Login')
        self.stdout.write('3. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            self.register_user()
        elif choice == '2':
            self.login_user()
        elif choice == '3':
            self.stdout.write('Exiting...')
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR('Invalid choice, try again.'))

    def show_user_menu(self):
        self.stdout.write(f'\nWelcome, {self.current_user.first_name} {self.current_user.last_name}!')
        self.stdout.write('1. Create Project')
        self.stdout.write('2. View All Projects')
        self.stdout.write('3. Edit My Project')
        self.stdout.write('4. Delete My Project')
        self.stdout.write('5. Search Projects by Date')
        self.stdout.write('6. Logout')
        choice = input('Enter your choice: ')
        if choice == '1':
            self.create_project()
        elif choice == '2':
            self.view_projects()
        elif choice == '3':
            self.edit_project()
        elif choice == '4':
            self.delete_project()
        elif choice == '5':
            self.search_projects_by_date()
        elif choice == '6':
            self.logout_user()
        else:
            self.stdout.write(self.style.ERROR('Invalid choice, try again.'))

    def register_user(self):
        self.stdout.write('\n==== User Registration ====')
        first_name = input('First Name: ')
        last_name = input('Last Name: ')
        email = input('Email: ')
        password1 = input('Password (min 8 chars): ')
        password2 = input('Confirm Password: ')
        mobile_phone = input('Mobile Phone (Egyptian, e.g., 01012345678): ')

        if password1 != password2:
            self.stdout.write(self.style.ERROR('Passwords do not match!'))
            return

        try:
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password1,
                mobile_phone=mobile_phone
            )
            self.stdout.write(self.style.SUCCESS('Registration successful!'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR('Email or mobile phone already exists!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def login_user(self):
        self.stdout.write('\n==== User Login ====')
        email = input('Email: ')
        password = input('Password: ')
        user = authenticate(username=email, password=password)
        if user is not None:
            self.current_user = user
            self.stdout.write(self.style.SUCCESS('Login successful!'))
        else:
            self.stdout.write(self.style.ERROR('Invalid email or password!'))

    def logout_user(self):
        self.current_user = None
        self.stdout.write(self.style.SUCCESS('Logout successful!'))

    def create_project(self):
        self.stdout.write('\n==== Create Project ====')
        title = input('Project Title: ')
        details = input('Project Details: ')
        total_target = input('Target Amount (EGP): ')
        start_date_str = input('Start Date (YYYY-MM-DD): ')
        end_date_str = input('End Date (YYYY-MM-DD): ')

        if not title or not details:
            self.stdout.write(self.style.ERROR('Title and Details cannot be empty!'))
            return

        try:
            total_target = float(total_target)
            if total_target <= 0:
                raise ValueError
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date <= start_date:
                self.stdout.write(self.style.ERROR('End date must be after start date!'))
                return
            Project.objects.create(
                title=title,
                details=details,
                total_target=total_target,
                start_date=start_date,
                end_date=end_date,
                owner=self.current_user
            )
            self.stdout.write(self.style.SUCCESS('Project created successfully!'))
        except ValueError:
            self.stdout.write(self.style.ERROR('Invalid amount or date format!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def view_projects(self):
        self.stdout.write('\n==== All Projects ====')
        projects = Project.objects.all()
        if not projects:
            self.stdout.write('No projects found.')
            return
        for project in projects:
            self.stdout.write(f'''
ID: {project.id}
Title: {project.title}
Details: {project.details}
Target Amount: {project.total_target} EGP
Start Date: {project.start_date}
End Date: {project.end_date}
Owner: {project.owner.first_name} {project.owner.last_name}
----------------------------------------
''')

    def edit_project(self):
        self.stdout.write('\n==== Edit My Project ====')
        my_projects = Project.objects.filter(owner=self.current_user)
        if not my_projects:
            self.stdout.write('You have no projects to edit.')
            return
        for project in my_projects:
            self.stdout.write(f'ID: {project.id}, Title: {project.title}')

        try:
            project_id = int(input('Enter project ID to edit: '))
            project = Project.objects.get(id=project_id, owner=self.current_user)

            new_title = input(f'New Title (current: {project.title}): ')
            new_details = input(f'New Details (current: {project.details}): ')
            new_target = input(f'New Target Amount (current: {project.total_target}): ')
            new_start = input(f'New Start Date (YYYY-MM-DD, current: {project.start_date}): ')
            new_end = input(f'New End Date (YYYY-MM-DD, current: {project.end_date}): ')

            if new_title:
                project.title = new_title
            if new_details:
                project.details = new_details
            if new_target:
                new_target_val = float(new_target)
                if new_target_val <= 0:
                    raise ValueError
                project.total_target = new_target_val
            if new_start:
                project.start_date = datetime.strptime(new_start, '%Y-%m-%d').date()
            if new_end:
                project.end_date = datetime.strptime(new_end, '%Y-%m-%d').date()

            if project.end_date <= project.start_date:
                self.stdout.write(self.style.ERROR('End date must be after start date!'))
                return

            project.save()
            self.stdout.write(self.style.SUCCESS('Project updated successfully!'))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('Project not found or you do not own it!'))
        except ValueError:
            self.stdout.write(self.style.ERROR('Invalid input!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def delete_project(self):
        self.stdout.write('\n==== Delete My Project ====')
        my_projects = Project.objects.filter(owner=self.current_user)
        if not my_projects:
            self.stdout.write('You have no projects to delete.')
            return
        for project in my_projects:
            self.stdout.write(f'ID: {project.id}, Title: {project.title}')

        try:
            project_id = int(input('Enter project ID to delete: '))
            project = Project.objects.get(id=project_id, owner=self.current_user)
            confirm = input(f'Are you sure you want to delete "{project.title}"? (y/n): ')
            if confirm.lower() == 'y':
                project.delete()
                self.stdout.write(self.style.SUCCESS('Project deleted successfully!'))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('Project not found or you do not own it!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def search_projects_by_date(self):
        self.stdout.write('\n==== Search Projects by Date ====')
        self.stdout.write('1. Search by Start Date')
        self.stdout.write('2. Search by End Date (before)')
        self.stdout.write('3. Search between two dates')
        choice = input('Enter your choice: ')
        try:
            if choice == '1':
                date_str = input('Enter Start Date (YYYY-MM-DD): ')
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                projects = Project.objects.filter(start_date=date)
            elif choice == '2':
                date_str = input('Enter End Date (YYYY-MM-DD): ')
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                projects = Project.objects.filter(end_date__lt=date)
            elif choice == '3':
                start_str = input('Enter Start Date (YYYY-MM-DD): ')
                end_str = input('Enter End Date (YYYY-MM-DD): ')
                start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
                projects = Project.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
            else:
                self.stdout.write(self.style.ERROR('Invalid choice!'))
                return

            if not projects:
                self.stdout.write('No projects found.')
                return
            for project in projects:
                self.stdout.write(f'''
ID: {project.id}
Title: {project.title}
Details: {project.details}
Target Amount: {project.total_target} EGP
Start Date: {project.start_date}
End Date: {project.end_date}
Owner: {project.owner.first_name} {project.owner.last_name}
----------------------------------------
''')
        except ValueError:
            self.stdout.write(self.style.ERROR('Invalid date format!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
