from account.models import BillFormat, BillingCycleSpecification, BillPresentationMedia
from account.repository import AccountRepository

# The bill structure is fixed for now: an e-mail bill in the standard format, every month.
PRESENTATION_MEDIA_ID = "BPM-1001"
FORMAT_ID = "BF-1001"
CYCLE_ID = "BCS-1001"


def load(repo: AccountRepository) -> None:
    # Reference data is seeded only into an empty database.
    if repo.has_reference_data():
        return
    repo.save_reference(
        [
            BillPresentationMedia(id=PRESENTATION_MEDIA_ID, name="Email", description="The bill is sent by e-mail"),
            BillFormat(id=FORMAT_ID, name="Standard", description="The standard bill layout"),
            BillingCycleSpecification(
                id=CYCLE_ID, name="Monthly", frequency="monthly", description="One bill every month"
            ),
        ]
    )
