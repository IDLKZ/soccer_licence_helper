"""
Entity Mapper
Конвертация между SQLAlchemy моделями и domain entities
"""
from typing import Optional, List
from app.domain.entities.user import User
from app.domain.entities.club import Club
from app.domain.entities.club_type import ClubType
from app.domain.entities.category_document import CategoryDocument
from app.domain.entities.season import Season
from app.domain.entities.league import League
from app.domain.entities.license import License
from app.domain.entities.application import Application
from app.domain.entities.application_criteria import ApplicationCriteria
from app.domain.entities.application_document import ApplicationDocument
from app.domain.entities.application_report import ApplicationReport

from app.infrastructure.database.models.user import UserModel
from app.infrastructure.database.models.club import ClubModel
from app.infrastructure.database.models.club_type import ClubTypeModel
from app.infrastructure.database.models.category_document import CategoryDocumentModel
from app.infrastructure.database.models.season import SeasonModel
from app.infrastructure.database.models.league import LeagueModel
from app.infrastructure.database.models.license import LicenseModel
from app.infrastructure.database.models.application import ApplicationModel
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.database.models.application_report import ApplicationReportModel


class EntityMapper:
    """Маппер для конвертации моделей в entities"""

    @staticmethod
    def to_user_entity(model: UserModel) -> User:
        """Конвертировать UserModel в User entity"""
        return User(
            id=model.id,
            email=model.email,
            phone=model.phone,
            username=model.username,
            password_hash=model.password,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            iin=model.iin,
            position=model.position,
            image_url=model.image_url,
            role_id=model.role_id,
            is_active=model.is_active,
            verified=model.verified,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_club_entity(model: ClubModel) -> Club:
        """Конвертировать ClubModel в Club entity"""
        return Club(
            id=model.id,
            image_url=model.image_url,
            parent_id=model.parent_id,
            type_id=model.type_id,
            full_name_ru=model.full_name_ru,
            full_name_kk=model.full_name_kk,
            full_name_en=model.full_name_en,
            short_name_ru=model.short_name_ru,
            short_name_kk=model.short_name_kk,
            short_name_en=model.short_name_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_category_document_entity(model: CategoryDocumentModel) -> CategoryDocument:
        """Конвертировать CategoryDocumentModel в CategoryDocument entity"""
        return CategoryDocument(
            id=model.id,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            value=model.value,
            level=model.level,
            role_ids=model.role_ids or [],
            role_values=model.role_values or [],
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_season_entity(model: SeasonModel) -> Season:
        """Конвертировать SeasonModel в Season entity"""
        return Season(
            id=model.id,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            start_date=model.start_date,
            end_date=model.end_date,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_league_entity(model: LeagueModel) -> League:
        """Конвертировать LeagueModel в League entity"""
        return League(
            id=model.id,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            level_ru=model.level_ru,
            level_kk=model.level_kk,
            level_en=model.level_en,
            level_value=model.level_value,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_license_entity(model: LicenseModel) -> License:
        """Конвертировать LicenseModel в License entity"""
        return License(
            id=model.id,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            season_id=model.season_id,
            league_id=model.league_id,
            start_date=model.start_at,  # В БД называется start_at
            end_date=model.end_at,      # В БД называется end_at
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_application_entity(model: ApplicationModel) -> Application:
        """Конвертировать ApplicationModel в Application entity"""
        return Application(
            id=model.id,
            club_id=model.club_id,
            license_id=model.license_id,
            status=model.status.value if hasattr(model.status, 'value') else model.status,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            description_ru=model.description_ru,
            description_kk=model.description_kk,
            description_en=model.description_en,
            notes=model.notes,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_application_criteria_entity(model: ApplicationCriteriaModel) -> ApplicationCriteria:
        """Конвертировать ApplicationCriteriaModel в ApplicationCriteria entity"""
        return ApplicationCriteria(
            id=model.id,
            application_id=model.application_id,
            category_id=model.category_id,
            first_checked_by=model.first_checked_by,
            first_checked_at=model.first_checked_at,
            first_check_status=model.first_check_status,
            first_check_comment=model.first_check_comment,
            checked_by=model.checked_by,
            checked_at=model.checked_at,
            check_status=model.check_status,
            check_comment=model.check_comment,
            control_checked_by=model.control_checked_by,
            control_checked_at=model.control_checked_at,
            control_check_status=model.control_check_status,
            control_check_comment=model.control_check_comment,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_application_document_entity(model: ApplicationDocumentModel) -> ApplicationDocument:
        """Конвертировать ApplicationDocumentModel в ApplicationDocument entity"""
        return ApplicationDocument(
            id=model.id,
            application_id=model.application_id,
            category_id=model.category_id,
            document_id=model.document_id,
            title_ru=model.title_ru,
            title_kk=model.title_kk,
            title_en=model.title_en,
            file_url=model.file_url,
            first_checked_by=model.first_checked_by,
            first_checked_at=model.first_checked_at,
            first_check_status=model.first_check_status,
            first_check_comment=model.first_check_comment,
            checked_by=model.checked_by,
            checked_at=model.checked_at,
            status=model.status,
            comment_ru=model.comment_ru,
            comment_kk=model.comment_kk,
            comment_en=model.comment_en,
            deadline=model.deadline,
            control_checked_by=model.control_checked_by,
            control_checked_at=model.control_checked_at,
            control_check_status=model.control_check_status,
            control_check_comment=model.control_check_comment,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_application_report_entity(model: ApplicationReportModel) -> ApplicationReport:
        """Конвертировать ApplicationReportModel в ApplicationReport entity"""
        return ApplicationReport(
            id=model.id,
            criteria_id=model.criteria_id,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
