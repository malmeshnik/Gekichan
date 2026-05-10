from typing import Optional, Union, Tuple
from rest_framework.exceptions import PermissionDenied
from apps.users.models import User
from .models import Project, ProjectMember

class ProjectService:
    @staticmethod
    def create_project(owner: User, name: str, description: Optional[str] = None) -> Project:
        project = Project.objects.create(
            owner=owner,
            name=name,
            description=description
        )
        # Create owner membership
        ProjectMember.objects.create(
            project=project,
            user=owner,
            role=ProjectMember.Role.OWNER
        )
        return project

    @staticmethod
    def add_member_by_username(owner: User, project_id: Union[str, int], username: str) -> Tuple[ProjectMember, bool]:
        project = Project.objects.get(id=project_id, owner=owner)
        user = User.objects.get(username=username)
        member, created = ProjectMember.objects.get_or_create(
            project=project,
            user=user,
            defaults={'role': ProjectMember.Role.MEMBER}
        )
        return member, created

    @staticmethod
    def add_member_by_id(owner: User, project_id: Union[str, int], user_id: int) -> Tuple[ProjectMember, bool]:
        project = Project.objects.get(id=project_id, owner=owner)
        user = User.objects.get(id=user_id)
        member, created = ProjectMember.objects.get_or_create(
            project=project,
            user=user,
            defaults={'role': ProjectMember.Role.MEMBER}
        )
        return member, created

    @staticmethod
    def delete_project(owner: User, project_id: Union[str, int]) -> bool:
        project = Project.objects.get(id=project_id, owner=owner)
        project.delete() # Soft delete
        return True
