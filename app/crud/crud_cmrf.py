from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cmrf_beneficiary import CmrfBeneficiary
from app.schemas.cmrf_beneficiary import CmrfBeneficiaryCreate, CmrfBeneficiaryUpdate


class CRUDCmrf(CRUDBase[CmrfBeneficiary, CmrfBeneficiaryCreate, CmrfBeneficiaryUpdate]):
    def create_masked(self, db: Session, *, obj_in: CmrfBeneficiaryCreate) -> CmrfBeneficiary:
        data = obj_in.model_dump(exclude={"aadhaar"})
        data["aadhaar_last4"] = obj_in.aadhaar[-4:]
        db_obj = CmrfBeneficiary(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


cmrf = CRUDCmrf(CmrfBeneficiary)
