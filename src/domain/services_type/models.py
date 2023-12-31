"""src/domain/services_type/models.py"""

from pydantic import Field

from src.domain.constants import Profession
from src.infrastructure.models import InternalModel, PublicModel

__all__ = (
    "ServiceTypeCreateRequestBody",
    "ServiceTypePublic",
    "ServiceTypeUncommited",
    "ServiceType",
)


# Public models
# ------------------------------------------------------
class ServiceTypeCreateRequestBody(PublicModel):
    """Service type create request body."""

    profession: Profession = Field(description="OpenAPI description")
    service_type: str = Field(description="OpenAPI description")


class ServiceTypePublic(ServiceTypeCreateRequestBody):
    """The public representation of the service type."""

    id: int


# Internal models
# ------------------------------------------------------
class ServiceTypeUncommited(InternalModel):
    """This schema is used for creating instance in the database."""

    profession: Profession
    service_type: str


class ServiceType(ServiceTypeUncommited):
    """Existed service type representation."""

    id: int
