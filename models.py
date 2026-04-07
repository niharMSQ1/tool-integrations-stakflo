from typing import Optional
import datetime
import uuid

from sqlalchemy import BigInteger, Boolean, CHAR, CheckConstraint, Date, DateTime, ForeignKeyConstraint, Identity, Index, Integer, JSON, PrimaryKeyConstraint, SmallInteger, String, Text, UniqueConstraint, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Cache(Base):
    __tablename__ = 'cache'
    __table_args__ = (
        PrimaryKeyConstraint('key', name='cache_pkey'),
    )

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    expiration: Mapped[int] = mapped_column(Integer, nullable=False)


class CacheLocks(Base):
    __tablename__ = 'cache_locks'
    __table_args__ = (
        PrimaryKeyConstraint('key', name='cache_locks_pkey'),
    )

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    expiration: Mapped[int] = mapped_column(Integer, nullable=False)


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='categories_pkey'),
        UniqueConstraint('name', name='categories_name_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    sub_categories: Mapped[list['SubCategories']] = relationship('SubCategories', back_populates='category')
    temp_vendors: Mapped[list['TempVendors']] = relationship('TempVendors', back_populates='category')
    vendors: Mapped[list['Vendors']] = relationship('Vendors', back_populates='category')


class CertificateDrafts(Base):
    __tablename__ = 'certificate_drafts'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='certificate_drafts_pkey'),
        Index('certificate_drafts_category_index', 'category'),
        Index('certificate_drafts_created_by_index', 'created_by'),
        Index('certificate_drafts_is_published_index', 'is_published'),
        Index('certificate_drafts_name_index', 'name'),
        Index('certificate_drafts_organization_id_index', 'organization_id'),
        Index('certificate_drafts_slug_index', 'slug')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    primary_domain: Mapped[Optional[str]] = mapped_column(String(255))
    secondary_domain: Mapped[Optional[str]] = mapped_column(String(255))
    labels: Mapped[Optional[dict]] = mapped_column(JSON)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    framework_import_drafts: Mapped[list['FrameworkImportDrafts']] = relationship('FrameworkImportDrafts', back_populates='certificate_draft')


class CertificateProviders(Base):
    __tablename__ = 'certificate_providers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='certificate_providers_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Certificates(Base):
    __tablename__ = 'certificates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='certificates_pkey'),
        UniqueConstraint('name', name='certificates_name_unique'),
        UniqueConstraint('slug', name='certificates_slug_unique'),
        Index('certificates_category_index', 'category'),
        Index('certificates_name_index', 'name'),
        Index('certificates_slug_index', 'slug')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    primary_domain: Mapped[Optional[str]] = mapped_column(String(255))
    secondary_domain: Mapped[Optional[str]] = mapped_column(String(255))
    labels: Mapped[Optional[dict]] = mapped_column(JSON)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    status: Mapped[Optional[str]] = mapped_column(String, server_default=text("'pending'::character varying"))

    audits: Mapped[list['Audits']] = relationship('Audits', back_populates='framework')
    clauses: Mapped[list['Clauses']] = relationship('Clauses', back_populates='certificate')
    framework_import_drafts: Mapped[list['FrameworkImportDrafts']] = relationship('FrameworkImportDrafts', back_populates='certificate')
    organization_certificates: Mapped[list['OrganizationCertificates']] = relationship('OrganizationCertificates', back_populates='certificate')
    vendor_assessment_question_banks: Mapped[list['VendorAssessmentQuestionBanks']] = relationship('VendorAssessmentQuestionBanks', back_populates='certificate')
    organization_certificate_clauses: Mapped[list['OrganizationCertificateClauses']] = relationship('OrganizationCertificateClauses', back_populates='certificate')
    organization_certificate_controls: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', back_populates='certificate')


class Comments(Base):
    __tablename__ = 'comments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='comments_pkey'),
        Index('comments_commentable_type_commentable_id_index', 'commentable_type', 'commentable_id'),
        Index('comments_commenter_type_commenter_id_index', 'commenter_type', 'commenter_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    commenter_type: Mapped[str] = mapped_column(String(255), nullable=False)
    commenter_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    commentable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    commentable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Controls(Base):
    __tablename__ = 'controls'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='controls_pkey'),
        UniqueConstraint('short_name', name='controls_short_name_unique'),
        Index('controls_category_index', 'category'),
        Index('controls_name_index', 'name'),
        Index('controls_short_name_index', 'short_name')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'0'::character varying"))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    level: Mapped[Optional[int]] = mapped_column(Integer)
    group: Mapped[Optional[str]] = mapped_column(String(255))
    frequency: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    internal_controls: Mapped[list['InternalControls']] = relationship('InternalControls', back_populates='control')
    organization_policy_control_mappings: Mapped[list['OrganizationPolicyControlMappings']] = relationship('OrganizationPolicyControlMappings', back_populates='control')
    policy_control_mappings: Mapped[list['PolicyControlMappings']] = relationship('PolicyControlMappings', back_populates='control')
    suggest_evidence_control_mappings: Mapped[list['SuggestEvidenceControlMappings']] = relationship('SuggestEvidenceControlMappings', back_populates='control')
    trustcenter_company_controls: Mapped[list['TrustcenterCompanyControls']] = relationship('TrustcenterCompanyControls', back_populates='control')
    control_clauses: Mapped[list['ControlClauses']] = relationship('ControlClauses', back_populates='control')
    control_scenarios: Mapped[list['ControlScenarios']] = relationship('ControlScenarios', back_populates='control')
    organization_certificate_controls: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', back_populates='control')
    risk_controls: Mapped[list['RiskControls']] = relationship('RiskControls', back_populates='control')
    control_evidence_master: Mapped[list['ControlEvidenceMaster']] = relationship('ControlEvidenceMaster', back_populates='control')


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='countries_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    iso3: Mapped[str] = mapped_column(String(255), nullable=False)
    iso2: Mapped[str] = mapped_column(String(255), nullable=False)
    phonecode: Mapped[str] = mapped_column(String(255), nullable=False)
    capital: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(255), nullable=False)
    currency_symbol: Mapped[str] = mapped_column(String(255), nullable=False)
    tld: Mapped[str] = mapped_column(String(255), nullable=False)
    region: Mapped[str] = mapped_column(String(255), nullable=False)
    subregion: Mapped[str] = mapped_column(String(255), nullable=False)
    timezones: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[str] = mapped_column(Text, nullable=False)
    longitude: Mapped[str] = mapped_column(Text, nullable=False)
    emoji: Mapped[str] = mapped_column(Text, nullable=False)
    emojiU: Mapped[str] = mapped_column(Text, nullable=False)
    flag: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    native: Mapped[Optional[str]] = mapped_column(String(255))
    translations: Mapped[Optional[str]] = mapped_column(Text)
    wikiDataId: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    states: Mapped[list['States']] = relationship('States', back_populates='country')


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_content_type_pkey'),
        UniqueConstraint('app_label', 'model', name='django_content_type_app_label_model_76bd3d3b_uniq')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    app_label: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)


class DjangoMigrations(Base):
    __tablename__ = 'django_migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='django_migrations_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    app: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    applied: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)


class FailedJobs(Base):
    __tablename__ = 'failed_jobs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='failed_jobs_pkey'),
        UniqueConstraint('uuid', name='failed_jobs_uuid_unique')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False)
    connection: Mapped[str] = mapped_column(Text, nullable=False)
    queue: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    exception: Mapped[str] = mapped_column(Text, nullable=False)
    failed_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False, server_default=text('CURRENT_TIMESTAMP'))


class Frameworks(Base):
    __tablename__ = 'frameworks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='frameworks_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class IntegrationDomains(Base):
    __tablename__ = 'integration_domains'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='domains_pkey'),
        UniqueConstraint('domain_group', 'evidence_sources', name='domains_domain_group_evidence_sources_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    domain_group: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    evidence_sources: Mapped[Optional[str]] = mapped_column(Text)
    primary_evidence: Mapped[Optional[str]] = mapped_column(Text)
    secondary_evidence: Mapped[Optional[str]] = mapped_column(Text)

    integration_domain_evidence_sources: Mapped[list['IntegrationDomainEvidenceSources']] = relationship('IntegrationDomainEvidenceSources', back_populates='integration_domain')
    tools: Mapped[list['Tools']] = relationship('Tools', back_populates='domain')


class JobBatches(Base):
    __tablename__ = 'job_batches'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='job_batches_pkey'),
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    total_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    pending_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_jobs: Mapped[int] = mapped_column(Integer, nullable=False)
    failed_job_ids: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    options: Mapped[Optional[str]] = mapped_column(Text)
    cancelled_at: Mapped[Optional[int]] = mapped_column(Integer)
    finished_at: Mapped[Optional[int]] = mapped_column(Integer)


class Jobs(Base):
    __tablename__ = 'jobs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='jobs_pkey'),
        Index('jobs_queue_index', 'queue')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    queue: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    attempts: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    available_at: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    reserved_at: Mapped[Optional[int]] = mapped_column(Integer)


class Migrations(Base):
    __tablename__ = 'migrations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='migrations_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    migration: Mapped[str] = mapped_column(String(255), nullable=False)
    batch: Mapped[int] = mapped_column(Integer, nullable=False)


class OauthAccessTokens(Base):
    __tablename__ = 'oauth_access_tokens'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='oauth_access_tokens_pkey'),
        Index('oauth_access_tokens_user_id_index', 'user_id')
    )

    id: Mapped[str] = mapped_column(CHAR(80), primary_key=True)
    client_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    scopes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class OauthClients(Base):
    __tablename__ = 'oauth_clients'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='oauth_clients_pkey'),
        Index('oauth_clients_owner_type_owner_id_index', 'owner_type', 'owner_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    redirect_uris: Mapped[str] = mapped_column(Text, nullable=False)
    grant_types: Mapped[str] = mapped_column(Text, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    personal_access_client: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    owner_type: Mapped[Optional[str]] = mapped_column(String(255))
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    secret: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    redirect: Mapped[Optional[str]] = mapped_column(Text)


class OauthDeviceCodes(Base):
    __tablename__ = 'oauth_device_codes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='oauth_device_codes_pkey'),
        UniqueConstraint('user_code', name='oauth_device_codes_user_code_unique'),
        Index('oauth_device_codes_client_id_index', 'client_id'),
        Index('oauth_device_codes_user_id_index', 'user_id')
    )

    id: Mapped[str] = mapped_column(CHAR(80), primary_key=True)
    client_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    user_code: Mapped[str] = mapped_column(CHAR(8), nullable=False)
    scopes: Mapped[str] = mapped_column(Text, nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    user_approved_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    last_polled_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class OauthRefreshTokens(Base):
    __tablename__ = 'oauth_refresh_tokens'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='oauth_refresh_tokens_pkey'),
        Index('oauth_refresh_tokens_access_token_id_index', 'access_token_id')
    )

    id: Mapped[str] = mapped_column(CHAR(80), primary_key=True)
    access_token_id: Mapped[str] = mapped_column(CHAR(80), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False)
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Organizations(Base):
    __tablename__ = 'organizations'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying]::text[])", name='organizations_status_check'),
        PrimaryKeyConstraint('id', name='organizations_pkey'),
        UniqueConstraint('domain_name', name='organizations_domain_name_unique'),
        UniqueConstraint('name', name='organizations_name_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'inactive'::character varying"))
    onboard: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    name: Mapped[Optional[str]] = mapped_column(String(250))
    domain_name: Mapped[Optional[str]] = mapped_column(String(250))
    short_name: Mapped[Optional[str]] = mapped_column(String(250))
    dark_logo: Mapped[Optional[str]] = mapped_column(String(250))
    light_logo: Mapped[Optional[str]] = mapped_column(String(250))
    primary_sector: Mapped[Optional[str]] = mapped_column(String(250))
    secondary_sectors: Mapped[Optional[dict]] = mapped_column(JSON)
    organization_size: Mapped[Optional[str]] = mapped_column(String(250))
    cloud_hosting_model: Mapped[Optional[str]] = mapped_column(String(250))
    types_of_data_handled: Mapped[Optional[dict]] = mapped_column(JSON)
    security_context: Mapped[Optional[dict]] = mapped_column(JSON)
    primary_country: Mapped[Optional[str]] = mapped_column(String(250))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    details_name: Mapped[Optional[str]] = mapped_column(String(250))
    details_organization_size: Mapped[Optional[str]] = mapped_column(String(250))
    details_primary_sector: Mapped[Optional[str]] = mapped_column(String(250))
    details_primary_country: Mapped[Optional[str]] = mapped_column(String(250))
    details_cloud_hosting_model: Mapped[Optional[str]] = mapped_column(String(250))
    details_types_of_data_handled: Mapped[Optional[dict]] = mapped_column(JSON)
    details_security_context: Mapped[Optional[dict]] = mapped_column(JSON)
    details_development_model: Mapped[Optional[str]] = mapped_column(String(250))
    details_product_service_description: Mapped[Optional[str]] = mapped_column(Text)

    assets: Mapped[list['Assets']] = relationship('Assets', back_populates='organization')
    auditors: Mapped[list['Auditors']] = relationship('Auditors', back_populates='organization')
    audits: Mapped[list['Audits']] = relationship('Audits', back_populates='organization')
    basic_settings: Mapped[Optional['BasicSettings']] = relationship('BasicSettings', uselist=False, back_populates='organization')
    data_subject_requests: Mapped[list['DataSubjectRequests']] = relationship('DataSubjectRequests', back_populates='organization')
    email_logs: Mapped[list['EmailLogs']] = relationship('EmailLogs', back_populates='organization')
    employee_import_batch_logs: Mapped[list['EmployeeImportBatchLogs']] = relationship('EmployeeImportBatchLogs', back_populates='organization')
    employee_import_staging: Mapped[list['EmployeeImportStaging']] = relationship('EmployeeImportStaging', back_populates='organization')
    employees: Mapped[list['Employees']] = relationship('Employees', back_populates='organization')
    framework_import_drafts: Mapped[list['FrameworkImportDrafts']] = relationship('FrameworkImportDrafts', back_populates='organization')
    integration_data: Mapped[list['IntegrationData']] = relationship('IntegrationData', back_populates='organization')
    notifications: Mapped[list['Notifications']] = relationship('Notifications', back_populates='organization')
    org_exe_policies: Mapped[list['OrgExePolicies']] = relationship('OrgExePolicies', back_populates='organization')
    org_policies: Mapped[list['OrgPolicies']] = relationship('OrgPolicies', back_populates='organization')
    organization_certificates: Mapped[list['OrganizationCertificates']] = relationship('OrganizationCertificates', back_populates='organization')
    organization_policies: Mapped[list['OrganizationPolicies']] = relationship('OrganizationPolicies', back_populates='organization')
    organization_policy_control_mappings: Mapped[list['OrganizationPolicyControlMappings']] = relationship('OrganizationPolicyControlMappings', back_populates='organization')
    reports: Mapped[list['Reports']] = relationship('Reports', back_populates='organization')
    risk_libraries: Mapped[list['RiskLibraries']] = relationship('RiskLibraries', back_populates='org')
    sso_setups: Mapped[list['SsoSetups']] = relationship('SsoSetups', back_populates='organization')
    temp_policy_uploads: Mapped[list['TempPolicyUploads']] = relationship('TempPolicyUploads', back_populates='organization')
    user_role_organizations: Mapped[list['UserRoleOrganizations']] = relationship('UserRoleOrganizations', back_populates='organization')
    user_web_tokens: Mapped[list['UserWebTokens']] = relationship('UserWebTokens', back_populates='organization')
    vendor_assessment_question_banks: Mapped[list['VendorAssessmentQuestionBanks']] = relationship('VendorAssessmentQuestionBanks', back_populates='organization')
    vulnerabilities: Mapped[list['Vulnerabilities']] = relationship('Vulnerabilities', back_populates='organization')
    organization_certificate_clauses: Mapped[list['OrganizationCertificateClauses']] = relationship('OrganizationCertificateClauses', back_populates='organization')
    organization_certificate_controls: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', back_populates='organization')
    organization_policy_clauses: Mapped[list['OrganizationPolicyClauses']] = relationship('OrganizationPolicyClauses', back_populates='organization')
    risk_registers: Mapped[list['RiskRegisters']] = relationship('RiskRegisters', back_populates='organization')
    tool_integrations: Mapped[list['ToolIntegrations']] = relationship('ToolIntegrations', back_populates='organization')
    organization_vendors: Mapped[list['OrganizationVendors']] = relationship('OrganizationVendors', back_populates='organization')
    evidence: Mapped[list['Evidence']] = relationship('Evidence', back_populates='organization')
    vendor_llm_processes: Mapped[list['VendorLlmProcesses']] = relationship('VendorLlmProcesses', back_populates='organization')


class PasswordResetTokens(Base):
    __tablename__ = 'password_reset_tokens'
    __table_args__ = (
        PrimaryKeyConstraint('email', name='password_reset_tokens_pkey'),
    )

    email: Mapped[str] = mapped_column(String(255), primary_key=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Permissions(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        ForeignKeyConstraint(['parent_id'], ['permissions.id'], ondelete='CASCADE', name='permissions_parent_id_foreign'),
        PrimaryKeyConstraint('id', name='permissions_pkey'),
        UniqueConstraint('name', name='permissions_name_unique'),
        Index('permissions_name_index', 'name')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    display_identifier: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    parent: Mapped[Optional['Permissions']] = relationship('Permissions', remote_side=[id], back_populates='parent_reverse')
    parent_reverse: Mapped[list['Permissions']] = relationship('Permissions', remote_side=[parent_id], back_populates='parent')
    role_permission: Mapped[list['RolePermission']] = relationship('RolePermission', back_populates='permission')


class PersonalAccessTokens(Base):
    __tablename__ = 'personal_access_tokens'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='personal_access_tokens_pkey'),
        UniqueConstraint('token', name='personal_access_tokens_token_unique'),
        Index('personal_access_tokens_expires_at_index', 'expires_at'),
        Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tokenable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    tokenable_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    token: Mapped[str] = mapped_column(String(64), nullable=False)
    abilities: Mapped[Optional[str]] = mapped_column(Text)
    last_used_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class PolicyTemplates(Base):
    __tablename__ = 'policy_templates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='policy_templates_pkey'),
        UniqueConstraint('short_name', name='policy_templates_short_name_unique'),
        Index('policy_templates_security_group_index', 'security_group'),
        Index('policy_templates_title_index', 'title')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    code: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    template: Mapped[Optional[str]] = mapped_column(Text)
    security_group: Mapped[Optional[str]] = mapped_column(String(255))
    group: Mapped[Optional[str]] = mapped_column(String(255))
    highlights: Mapped[Optional[dict]] = mapped_column(JSON)
    version: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization_policies: Mapped[list['OrganizationPolicies']] = relationship('OrganizationPolicies', back_populates='policy_template')
    organization_policy_control_mappings: Mapped[list['OrganizationPolicyControlMappings']] = relationship('OrganizationPolicyControlMappings', back_populates='policy_template')
    policy_control_mappings: Mapped[list['PolicyControlMappings']] = relationship('PolicyControlMappings', back_populates='policy_template')
    evidence_masters: Mapped[list['EvidenceMasters']] = relationship('EvidenceMasters', back_populates='policy_template')
    organization_policy_clauses: Mapped[list['OrganizationPolicyClauses']] = relationship('OrganizationPolicyClauses', back_populates='policy_template')
    policy_clauses: Mapped[list['PolicyClauses']] = relationship('PolicyClauses', back_populates='policy_template')


class Roles(Base):
    __tablename__ = 'roles'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying]::text[])", name='roles_status_check'),
        PrimaryKeyConstraint('id', name='roles_pkey'),
        UniqueConstraint('name', name='roles_name_unique'),
        Index('roles_name_index', 'name')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'active'::character varying"))
    guard_name: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    role_permission: Mapped[list['RolePermission']] = relationship('RolePermission', back_populates='role')
    user_role_organizations: Mapped[list['UserRoleOrganizations']] = relationship('UserRoleOrganizations', back_populates='role')


class Sessions(Base):
    __tablename__ = 'sessions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sessions_pkey'),
        Index('sessions_last_activity_index', 'last_activity'),
        Index('sessions_user_id_index', 'user_id')
    )

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    payload: Mapped[str] = mapped_column(Text, nullable=False)
    last_activity: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)


class SsoProviders(Base):
    __tablename__ = 'sso_providers'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying]::text[])", name='sso_providers_status_check'),
        PrimaryKeyConstraint('id', name='sso_providers_pkey'),
        UniqueConstraint('name', name='sso_providers_name_unique'),
        UniqueConstraint('slug', name='sso_providers_slug_unique'),
        Index('sso_providers_slug_index', 'slug')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'inactive'::character varying"))
    configuration_keys: Mapped[Optional[dict]] = mapped_column(JSON)
    image_path: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    sso_setups: Mapped[list['SsoSetups']] = relationship('SsoSetups', back_populates='sso_provider')


class SuggestEvidence(Base):
    __tablename__ = 'suggest_evidence'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='suggest_evidence_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'active'::character varying"))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    suggest_evidence_control_mappings: Mapped[list['SuggestEvidenceControlMappings']] = relationship('SuggestEvidenceControlMappings', back_populates='suggest_evidence')


class TrustCenterConfigs(Base):
    __tablename__ = 'trust_center_configs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='trust_center_configs_pkey'),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    status: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('1'))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class TrustCenters(Base):
    __tablename__ = 'trust_centers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='trust_centers_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    privacy_url: Mapped[Optional[str]] = mapped_column(String(255))
    terms_url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class TrustcenterCompanies(Base):
    __tablename__ = 'trustcenter_companies'
    __table_args__ = (
        CheckConstraint("domain_type::text = ANY (ARRAY['CNAME'::character varying, 'A'::character varying]::text[])", name='trustcenter_companies_domain_type_check'),
        PrimaryKeyConstraint('id', name='trustcenter_companies_pkey'),
        UniqueConstraint('name', name='trustcenter_companies_name_unique'),
        UniqueConstraint('slug', name='trustcenter_companies_slug_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    plan: Mapped[str] = mapped_column(String(64), nullable=False, server_default=text("'free'::character varying"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    support_email: Mapped[Optional[str]] = mapped_column(String(255))
    aws_access_key_id: Mapped[Optional[str]] = mapped_column(String(255))
    aws_secret_access_key: Mapped[Optional[str]] = mapped_column(Text)
    aws_region: Mapped[Optional[str]] = mapped_column(String(64), server_default=text("'us-east-1'::character varying"))
    azure_client_id: Mapped[Optional[str]] = mapped_column(String(255))
    azure_client_secret: Mapped[Optional[str]] = mapped_column(Text)
    azure_tenant_id: Mapped[Optional[str]] = mapped_column(String(255))
    azure_subscription_id: Mapped[Optional[str]] = mapped_column(String(255))
    gcp_project_id: Mapped[Optional[str]] = mapped_column(String(255))
    gcp_service_account_key: Mapped[Optional[str]] = mapped_column(Text)
    custom_domain: Mapped[Optional[str]] = mapped_column(String(255))
    domain_type: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'CNAME'::character varying"))
    domain_ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    trustcenter_access_requests: Mapped[list['TrustcenterAccessRequests']] = relationship('TrustcenterAccessRequests', back_populates='company')
    trustcenter_certifications: Mapped[list['TrustcenterCertifications']] = relationship('TrustcenterCertifications', back_populates='company')
    trustcenter_company_controls: Mapped[list['TrustcenterCompanyControls']] = relationship('TrustcenterCompanyControls', back_populates='company')
    trustcenter_faqs: Mapped[list['TrustcenterFaqs']] = relationship('TrustcenterFaqs', back_populates='company')
    trustcenter_leadership: Mapped[list['TrustcenterLeadership']] = relationship('TrustcenterLeadership', back_populates='company')
    trustcenter_subprocessors: Mapped[list['TrustcenterSubprocessors']] = relationship('TrustcenterSubprocessors', back_populates='company')
    trustcenter_users: Mapped[list['TrustcenterUsers']] = relationship('TrustcenterUsers', back_populates='company_')


class TrustcenterContactRequests(Base):
    __tablename__ = 'trustcenter_contact_requests'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'read'::character varying, 'replied'::character varying, 'archived'::character varying]::text[])", name='trustcenter_contact_requests_status_check'),
        PrimaryKeyConstraint('id', name='trustcenter_contact_requests_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class TrustcenterControls(Base):
    __tablename__ = 'trustcenter_controls'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='trustcenter_controls_pkey'),
        UniqueConstraint('short_name', name='trustcenter_controls_short_name_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    short_name: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'0'::character varying"))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    level: Mapped[Optional[int]] = mapped_column(Integer)
    group: Mapped[Optional[str]] = mapped_column(String(255))
    frequency: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class TrustcenterPlans(Base):
    __tablename__ = 'trustcenter_plans'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='trustcenter_plans_pkey'),
        UniqueConstraint('key', name='trustcenter_plans_key_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    key: Mapped[str] = mapped_column(String(64), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    features: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    price: Mapped[Optional[str]] = mapped_column(String(64))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_unique'),
        Index('users_company_id_index', 'company_id'),
        Index('users_product_index', 'product')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    two_factor_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    welcome_popup_seen: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    google2fa_secret: Mapped[Optional[str]] = mapped_column(Text)
    email_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    provider_id: Mapped[Optional[str]] = mapped_column(String(255))
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    last_initial_page: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    product: Mapped[Optional[str]] = mapped_column(String(255))
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    company: Mapped[Optional[str]] = mapped_column(String(255))
    role: Mapped[Optional[str]] = mapped_column(String(255))
    verification_code_hash: Mapped[Optional[str]] = mapped_column(String(255))
    verification_expires: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    reset_token: Mapped[Optional[str]] = mapped_column(String(255))
    reset_token_expires: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    audits: Mapped[list['Audits']] = relationship('Audits', back_populates='poc')
    data_subject_requests: Mapped[list['DataSubjectRequests']] = relationship('DataSubjectRequests', back_populates='users')
    employee_import_batch_logs: Mapped[list['EmployeeImportBatchLogs']] = relationship('EmployeeImportBatchLogs', back_populates='users')
    employees: Mapped[list['Employees']] = relationship('Employees', back_populates='sync_user')
    framework_import_drafts: Mapped[list['FrameworkImportDrafts']] = relationship('FrameworkImportDrafts', back_populates='users')
    internal_controls: Mapped[list['InternalControls']] = relationship('InternalControls', back_populates='owner')
    org_policies: Mapped[list['OrgPolicies']] = relationship('OrgPolicies', foreign_keys='[OrgPolicies.created_by]', back_populates='users')
    org_policies_: Mapped[list['OrgPolicies']] = relationship('OrgPolicies', foreign_keys='[OrgPolicies.created_by_id]', back_populates='created_by_')
    temp_policy_uploads: Mapped[list['TempPolicyUploads']] = relationship('TempPolicyUploads', back_populates='users')
    temp_tasks: Mapped[list['TempTasks']] = relationship('TempTasks', back_populates='owner')
    audit_clause_statuses: Mapped[list['AuditClauseStatuses']] = relationship('AuditClauseStatuses', back_populates='auditor')
    organization_certificate_controls: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', foreign_keys='[OrganizationCertificateControls.assigned_by]', back_populates='users')
    organization_certificate_controls_: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', foreign_keys='[OrganizationCertificateControls.assignee_id]', back_populates='assignee')
    policy_versions: Mapped[list['PolicyVersions']] = relationship('PolicyVersions', back_populates='users')
    risk_registers: Mapped[list['RiskRegisters']] = relationship('RiskRegisters', back_populates='owner')
    tool_integrations: Mapped[list['ToolIntegrations']] = relationship('ToolIntegrations', back_populates='user')
    organization_internal_controls: Mapped[list['OrganizationInternalControls']] = relationship('OrganizationInternalControls', back_populates='owner')
    policy_approvers: Mapped[list['PolicyApprovers']] = relationship('PolicyApprovers', back_populates='approver')


class VendorAssessmentQuestionBankTemps(Base):
    __tablename__ = 'vendor_assessment_question_bank_temps'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vendor_assessment_question_bank_temps_pkey'),
        Index('vendor_assessment_question_bank_temps_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    certificate_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    vendor_type: Mapped[Optional[str]] = mapped_column(String(255))
    department: Mapped[Optional[str]] = mapped_column(String(255))
    question: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(255))
    data_exposure: Mapped[Optional[str]] = mapped_column(String(255))
    weightage: Mapped[Optional[dict]] = mapped_column(JSON)
    is_attachment: Mapped[Optional[dict]] = mapped_column(JSON, server_default=text("'[]'::json"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class VendorCertificateDocuments(Base):
    __tablename__ = 'vendor_certificate_documents'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vendor_certificate_documents_pkey'),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_certificate_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class Assets(Base):
    __tablename__ = 'assets'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='assets_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='assets_pkey'),
        Index('assets_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    platform: Mapped[Optional[str]] = mapped_column(String(255))
    scope: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    host_name: Mapped[Optional[str]] = mapped_column(String(255))
    os_name: Mapped[Optional[str]] = mapped_column(String(255))
    os_version: Mapped[Optional[str]] = mapped_column(String(255))
    ip_address: Mapped[Optional[str]] = mapped_column(String(255))
    port: Mapped[Optional[str]] = mapped_column(String(255))
    protocol: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[Optional[str]] = mapped_column(String(255))
    tags: Mapped[Optional[str]] = mapped_column(String(255))
    agent_check_in: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='assets')


class Auditors(Base):
    __tablename__ = 'auditors'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='auditors_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='auditors_pkey'),
        UniqueConstraint('organization_id', 'email', name='auditors_organization_id_email_unique'),
        Index('auditors_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    remember_token: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='auditors')


class Audits(Base):
    __tablename__ = 'audits'
    __table_args__ = (
        ForeignKeyConstraint(['framework_id'], ['certificates.id'], ondelete='RESTRICT', onupdate='CASCADE', name='audits_framework_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='audits_organization_id_foreign'),
        ForeignKeyConstraint(['poc_id'], ['users.id'], ondelete='RESTRICT', onupdate='CASCADE', name='audits_poc_id_foreign'),
        PrimaryKeyConstraint('id', name='audits_pkey'),
        Index('audits_end_date_index', 'end_date'),
        Index('audits_framework_id_index', 'framework_id'),
        Index('audits_organization_id_index', 'organization_id'),
        Index('audits_poc_id_index', 'poc_id'),
        Index('audits_start_date_index', 'start_date'),
        Index('audits_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    audit_type: Mapped[str] = mapped_column(String(255), nullable=False)
    audit_title: Mapped[str] = mapped_column(String(255), nullable=False)
    framework_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    poc_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    auditor_organization: Mapped[Optional[str]] = mapped_column(String(255))
    scope_details: Mapped[Optional[dict]] = mapped_column(JSONB)
    access_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    access_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    framework: Mapped['Certificates'] = relationship('Certificates', back_populates='audits')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='audits')
    poc: Mapped['Users'] = relationship('Users', back_populates='audits')
    audit_clause_statuses: Mapped[list['AuditClauseStatuses']] = relationship('AuditClauseStatuses', back_populates='audit')
    audit_mappings: Mapped[list['AuditMappings']] = relationship('AuditMappings', back_populates='audit')


class BasicSettings(Base):
    __tablename__ = 'basic_settings'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='basic_settings_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='basic_settings_pkey'),
        UniqueConstraint('organization_id', name='basic_settings_organization_id_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    language: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'en'::character varying"))
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("'Asia/Kolkata'::character varying"))
    date_format: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'d-m-Y'::character varying"))
    time_format: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'H:i'::character varying"))
    number_format: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'1,234.56'::character varying"))
    currency: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'INR'::character varying"))
    currency_symbol: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'₹'::character varying"))
    theme_mode: Mapped[str] = mapped_column(String(10), nullable=False, server_default=text("'light'::character varying"))
    maintenance_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    default_landing_page: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='basic_settings')


class Clauses(Base):
    __tablename__ = 'clauses'
    __table_args__ = (
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', onupdate='CASCADE', name='clauses_certificate_id_foreign'),
        ForeignKeyConstraint(['parent_id'], ['clauses.id'], ondelete='CASCADE', onupdate='CASCADE', name='clauses_parent_id_foreign'),
        PrimaryKeyConstraint('id', name='clauses_pkey'),
        Index('clauses_certificate_id_index', 'certificate_id'),
        Index('clauses_parent_id_index', 'parent_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    certificate_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    reference_id: Mapped[str] = mapped_column(String(255), nullable=False)
    display_identifier: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    certificate: Mapped['Certificates'] = relationship('Certificates', back_populates='clauses')
    parent: Mapped[Optional['Clauses']] = relationship('Clauses', remote_side=[id], back_populates='parent_reverse')
    parent_reverse: Mapped[list['Clauses']] = relationship('Clauses', remote_side=[parent_id], back_populates='parent')
    audit_clause_statuses: Mapped[list['AuditClauseStatuses']] = relationship('AuditClauseStatuses', back_populates='clause')
    control_clauses: Mapped[list['ControlClauses']] = relationship('ControlClauses', back_populates='clause')
    organization_certificate_clauses: Mapped[list['OrganizationCertificateClauses']] = relationship('OrganizationCertificateClauses', back_populates='clause')
    organization_certificate_controls: Mapped[list['OrganizationCertificateControls']] = relationship('OrganizationCertificateControls', back_populates='clause')
    organization_policy_clauses: Mapped[list['OrganizationPolicyClauses']] = relationship('OrganizationPolicyClauses', back_populates='clause')
    policy_clauses: Mapped[list['PolicyClauses']] = relationship('PolicyClauses', back_populates='clause')


class DataSubjectRequests(Base):
    __tablename__ = 'data_subject_requests'
    __table_args__ = (
        CheckConstraint("request_type::text = ANY (ARRAY['access_my_personal_data'::character varying, 'correct_my_personal_data'::character varying, 'delete_my_personal_data'::character varying, 'restrict_how_my_personal_data_is_used'::character varying, 'receive_a_copy_of_my_personal_data'::character varying, 'object_to_the_use_of_my_personal_data'::character varying, 'opt_out_of_the_sale_or_sharing_of_my_personal_data'::character varying, 'other_my_data_request'::character varying]::text[])", name='data_subject_requests_request_type_check'),
        CheckConstraint("status::text = ANY (ARRAY['requested'::character varying, 'identity_pending'::character varying, 'in_progress'::character varying, 'on_hold'::character varying, 'completed'::character varying, 'rejected'::character varying]::text[])", name='data_subject_requests_status_check'),
        ForeignKeyConstraint(['assigned_to'], ['users.id'], ondelete='SET NULL', name='data_subject_requests_assigned_to_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='SET NULL', name='data_subject_requests_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='data_subject_requests_pkey'),
        Index('data_subject_requests_email_index', 'email'),
        Index('data_subject_requests_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    request_type: Mapped[str] = mapped_column(String(255), nullable=False)
    identity_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'requested'::character varying"))
    requested_date: Mapped[datetime.date] = mapped_column(Date, nullable=False, server_default=text("'2026-03-18'::date"))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    organization_name: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    relationship_with: Mapped[Optional[str]] = mapped_column(String(255))
    if_other_relationship: Mapped[Optional[str]] = mapped_column(String(255))
    request_details: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(String(255))
    identity_verified_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    assigned_to: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    assigned_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    completed_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    internal_notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='data_subject_requests')
    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='data_subject_requests')


class EmailLogs(Base):
    __tablename__ = 'email_logs'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['queued'::character varying, 'sent'::character varying, 'failed'::character varying]::text[])", name='email_logs_status_check'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='SET NULL', name='email_logs_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='email_logs_pkey'),
        Index('email_logs_emailable_type_emailable_id_index', 'emailable_type', 'emailable_id'),
        Index('email_logs_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    to_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'queued'::character varying"))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    subject: Mapped[Optional[str]] = mapped_column(String(255))
    mailable: Mapped[Optional[str]] = mapped_column(String(255))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    emailable_type: Mapped[Optional[str]] = mapped_column(String(255))
    emailable_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    queued_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    failed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='email_logs')


class EmployeeImportBatchLogs(Base):
    __tablename__ = 'employee_import_batch_logs'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='employee_import_batch_logs_organization_id_foreign'),
        ForeignKeyConstraint(['uploaded_by'], ['users.id'], ondelete='SET NULL', name='employee_import_batch_logs_uploaded_by_foreign'),
        PrimaryKeyConstraint('id', name='employee_import_batch_logs_pkey'),
        UniqueConstraint('import_batch_id', name='employee_import_batch_logs_import_batch_id_unique'),
        Index('employee_import_batch_logs_organization_id_index', 'organization_id'),
        Index('employee_import_batch_logs_uploaded_by_index', 'uploaded_by')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    import_batch_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    staged: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    skipped: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    skipped_rows_total: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    response_payload_truncated: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    uploaded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    skipped_reason_summary: Mapped[Optional[dict]] = mapped_column(JSON)
    skipped_rows: Mapped[Optional[dict]] = mapped_column(JSON)
    duplicate_emails: Mapped[Optional[dict]] = mapped_column(JSON)
    original_filename: Mapped[Optional[str]] = mapped_column(String(512))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='employee_import_batch_logs')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='employee_import_batch_logs')


class EmployeeImportStaging(Base):
    __tablename__ = 'employee_import_staging'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='employee_import_staging_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='employee_import_staging_pkey'),
        Index('employee_import_staging_import_batch_id_index', 'import_batch_id'),
        Index('employee_import_staging_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    import_batch_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[int] = mapped_column(SmallInteger, nullable=False, server_default=text("'0'::smallint"))
    uploaded_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sync_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    department: Mapped[Optional[str]] = mapped_column(String(255))
    designation: Mapped[Optional[str]] = mapped_column(String(255))
    employee_id: Mapped[Optional[str]] = mapped_column(String(255))
    employee_type: Mapped[Optional[str]] = mapped_column(String(255))
    employee_status: Mapped[Optional[str]] = mapped_column(String(255))
    marital_status: Mapped[Optional[str]] = mapped_column(String(255))
    gender: Mapped[Optional[str]] = mapped_column(String(255))
    source_of_hire: Mapped[Optional[str]] = mapped_column(String(255))
    date_of_joining: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_of_exit: Mapped[Optional[datetime.date]] = mapped_column(Date)
    date_of_birth: Mapped[Optional[datetime.date]] = mapped_column(Date)
    current_experience: Mapped[Optional[str]] = mapped_column(String(255))
    total_experience: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    zip_code: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_relationship: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    image: Mapped[Optional[str]] = mapped_column(String(512))
    provided_fields: Mapped[Optional[dict]] = mapped_column(JSON)

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='employee_import_staging')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='employees_organization_id_foreign'),
        ForeignKeyConstraint(['sync_user_id'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='employees_sync_user_id_foreign'),
        PrimaryKeyConstraint('id', name='employees_pkey'),
        UniqueConstraint('organization_id', 'email', name='employees_organization_id_email_unique'),
        Index('employees_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    has_changed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    sync_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    image: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    provider_id: Mapped[Optional[str]] = mapped_column(String(255))
    employee_id: Mapped[Optional[str]] = mapped_column(String(255))
    department: Mapped[Optional[str]] = mapped_column(String(255))
    designation: Mapped[Optional[str]] = mapped_column(String(255))
    employee_status: Mapped[Optional[str]] = mapped_column(String(255))
    employee_type: Mapped[Optional[str]] = mapped_column(String(255))
    marital_status: Mapped[Optional[str]] = mapped_column(String(255))
    gender: Mapped[Optional[str]] = mapped_column(String(255))
    source_of_hire: Mapped[Optional[str]] = mapped_column(String(255))
    date_of_joining: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    date_of_exit: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    date_of_birth: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    current_experience: Mapped[Optional[str]] = mapped_column(String(255))
    total_experience: Mapped[Optional[str]] = mapped_column(String(255))
    remember_token: Mapped[Optional[str]] = mapped_column(String(100))
    changed_values: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    zip_code: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(255))
    emergency_contact_relationship: Mapped[Optional[str]] = mapped_column(String(255))
    last_synced_at: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    reg_status: Mapped[Optional[str]] = mapped_column(String)
    login_status: Mapped[Optional[int]] = mapped_column(Integer)

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='employees')
    sync_user: Mapped[Optional['Users']] = relationship('Users', back_populates='employees')


class FrameworkImportDrafts(Base):
    __tablename__ = 'framework_import_drafts'
    __table_args__ = (
        ForeignKeyConstraint(['certificate_draft_id'], ['certificate_drafts.id'], ondelete='CASCADE', name='framework_import_drafts_certificate_draft_id_foreign'),
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', name='framework_import_drafts_certificate_id_foreign'),
        ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL', name='framework_import_drafts_created_by_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='framework_import_drafts_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='framework_import_drafts_pkey'),
        Index('framework_import_drafts_organization_id_certificate_id_index', 'organization_id', 'certificate_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    import_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'draft'::character varying"))
    certificate_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    certificate_draft_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    certificate_draft: Mapped[Optional['CertificateDrafts']] = relationship('CertificateDrafts', back_populates='framework_import_drafts')
    certificate: Mapped[Optional['Certificates']] = relationship('Certificates', back_populates='framework_import_drafts')
    users: Mapped[Optional['Users']] = relationship('Users', back_populates='framework_import_drafts')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='framework_import_drafts')


class IntegrationData(Base):
    __tablename__ = 'integration_data'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='integration_data_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='integration_data_pkey'),
        UniqueConstraint('platform', 'external_id', 'organization_id', name='unique_platform_external_org')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    fetched_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    platform: Mapped[Optional[str]] = mapped_column(String(50))
    scope: Mapped[Optional[str]] = mapped_column(String(50))
    external_id: Mapped[Optional[str]] = mapped_column(String(255))
    data: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='integration_data')


class IntegrationDomainEvidenceSources(Base):
    __tablename__ = 'integration_domain_evidence_sources'
    __table_args__ = (
        ForeignKeyConstraint(['integration_domain_id'], ['integration_domains.id'], ondelete='CASCADE', name='integration_domain_evidence_sources_integration_domain_id_fkey'),
        PrimaryKeyConstraint('id', name='integration_domain_evidence_sources_pkey'),
        Index('integration_domain_evidence_sources_evidence_source_key', 'evidence_source', unique=True),
        Index('integration_domain_evidence_sources_integration_domain_id_idx', 'integration_domain_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    integration_domain_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    evidence_source: Mapped[str] = mapped_column(Text, nullable=False)
    primary_evidence: Mapped[Optional[str]] = mapped_column(Text)
    secondary_evidence: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('now()'))

    integration_domain: Mapped['IntegrationDomains'] = relationship('IntegrationDomains', back_populates='integration_domain_evidence_sources')
    evidence_masters: Mapped[list['EvidenceMasters']] = relationship('EvidenceMasters', back_populates='integration_domain_evidence_sources')


class InternalControls(Base):
    __tablename__ = 'internal_controls'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='internal_controls_control_id_foreign'),
        ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE', name='internal_controls_owner_id_foreign'),
        PrimaryKeyConstraint('id', name='internal_controls_pkey'),
        Index('internal_controls_control_id_index', 'control_id'),
        Index('internal_controls_owner_id_index', 'owner_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    evidence_required: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'active'::character varying"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    frequency: Mapped[Optional[str]] = mapped_column(String(255))
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    metadata_: Mapped[Optional[dict]] = mapped_column('metadata', JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='internal_controls')
    owner: Mapped[Optional['Users']] = relationship('Users', back_populates='internal_controls')
    organization_internal_controls: Mapped[list['OrganizationInternalControls']] = relationship('OrganizationInternalControls', back_populates='internal_control')


class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='notifications_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='notifications_pkey'),
        Index('notifications_notifiable_type_notifiable_id_read_at_index', 'notifiable_type', 'notifiable_id', 'read_at'),
        Index('notifications_organization_id_read_at_index', 'organization_id', 'read_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    notifiable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    notifiable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'info'::character varying"))
    message: Mapped[Optional[str]] = mapped_column(Text)
    data: Mapped[Optional[dict]] = mapped_column(JSON)
    read_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='notifications')


class OrgExePolicies(Base):
    __tablename__ = 'org_exe_policies'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='org_exe_policies_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='org_exe_policies_pkey'),
        Index('org_exe_policies_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    file_path: Mapped[Optional[str]] = mapped_column(String(255))
    executed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='org_exe_policies')


class OrgPolicies(Base):
    __tablename__ = 'org_policies'
    __table_args__ = (
        CheckConstraint("policy_type::text = ANY (ARRAY['orgpolicy'::character varying, 'existingpolicy'::character varying]::text[])", name='org_policies_policy_type_check'),
        CheckConstraint("status::text = ANY (ARRAY['initialising'::character varying, 'initiated'::character varying, 'generated'::character varying]::text[])", name='org_policies_status_check'),
        ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE', name='org_policies_created_by_foreign'),
        ForeignKeyConstraint(['created_by_id'], ['users.id'], ondelete='CASCADE', name='org_policies_created_by_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='org_policies_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='org_policies_pkey'),
        Index('org_policies_organization_id_index', 'organization_id'),
        Index('org_policies_title_index', 'title')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'initialising'::character varying"))
    created_by_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    policy_type: Mapped[Optional[str]] = mapped_column(String(255))
    template: Mapped[Optional[str]] = mapped_column(Text)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    department: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    workforce_assignments: Mapped[Optional[dict]] = mapped_column(JSON)
    effective_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[created_by], back_populates='org_policies')
    created_by_: Mapped['Users'] = relationship('Users', foreign_keys=[created_by_id], back_populates='org_policies_')
    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='org_policies')
    policy_versions: Mapped[list['PolicyVersions']] = relationship('PolicyVersions', back_populates='org_policy')


class OrganizationCertificates(Base):
    __tablename__ = 'organization_certificates'
    __table_args__ = (
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', name='organization_certificates_certificate_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='organization_certificates_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_certificates_pkey'),
        UniqueConstraint('organization_id', 'certificate_id', name='org_cert_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    certificate_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    labels: Mapped[Optional[dict]] = mapped_column(JSON)
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    certificate: Mapped['Certificates'] = relationship('Certificates', back_populates='organization_certificates')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_certificates')


class OrganizationPolicies(Base):
    __tablename__ = 'organization_policies'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policies_organization_id_foreign'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policies_policy_template_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_policies_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    policy_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    custom_policy_doc: Mapped[Optional[str]] = mapped_column(Text)
    custom_policy_version: Mapped[Optional[str]] = mapped_column(Text)
    custom_policy_template: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_policies')
    policy_template: Mapped['PolicyTemplates'] = relationship('PolicyTemplates', back_populates='organization_policies')


class OrganizationPolicyControlMappings(Base):
    __tablename__ = 'organization_policy_control_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_control_mappings_control_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_control_mappings_organization_id_foreign'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_control_mappings_policy_template_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_policy_control_mappings_pkey'),
        UniqueConstraint('organization_id', 'policy_template_id', 'control_id', name='organization_policy_control_mappings_organization_id_policy_tem'),
        Index('organization_policy_control_mappings_control_id_index', 'control_id'),
        Index('organization_policy_control_mappings_policy_template_id_index', 'policy_template_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    policy_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='organization_policy_control_mappings')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_policy_control_mappings')
    policy_template: Mapped['PolicyTemplates'] = relationship('PolicyTemplates', back_populates='organization_policy_control_mappings')


class PolicyControlMappings(Base):
    __tablename__ = 'policy_control_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', onupdate='CASCADE', name='policy_control_mappings_control_id_foreign'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='CASCADE', onupdate='CASCADE', name='policy_control_mappings_policy_template_id_foreign'),
        PrimaryKeyConstraint('id', name='policy_control_mappings_pkey'),
        UniqueConstraint('policy_template_id', 'control_id', name='policy_control_mappings_policy_template_id_control_id_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    policy_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='policy_control_mappings')
    policy_template: Mapped['PolicyTemplates'] = relationship('PolicyTemplates', back_populates='policy_control_mappings')


class Reports(Base):
    __tablename__ = 'reports'
    __table_args__ = (
        CheckConstraint("export_format::text = ANY (ARRAY['PDF'::character varying, 'CSV'::character varying, 'JSON'::character varying]::text[])", name='reports_export_format_check'),
        CheckConstraint("report_type::text = ANY (ARRAY['Risk'::character varying, 'Vendor'::character varying, 'Policy'::character varying, 'Audit'::character varying]::text[])", name='reports_report_type_check'),
        CheckConstraint("status::text = ANY (ARRAY['Ready'::character varying, 'Processing'::character varying, 'Failed'::character varying]::text[])", name='reports_status_check'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='reports_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='reports_pkey'),
        Index('reports_created_at_index', 'created_at'),
        Index('reports_generated_by_index', 'generated_by'),
        Index('reports_organization_id_index', 'organization_id'),
        Index('reports_type_index', 'report_type')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    report_title: Mapped[str] = mapped_column(String(255), nullable=False)
    report_type: Mapped[str] = mapped_column(String(255), nullable=False)
    export_format: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'JSON'::character varying"))
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'Ready'::character varying"))
    start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    report_data: Mapped[Optional[dict]] = mapped_column(JSON)
    file_path: Mapped[Optional[str]] = mapped_column(String(255))
    generated_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='reports')


class RiskLibraries(Base):
    __tablename__ = 'risk_libraries'
    __table_args__ = (
        ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='risk_libraries_org_id_foreign'),
        PrimaryKeyConstraint('id', name='risk_libraries_pkey'),
        Index('risk_libraries_org_id_index', 'org_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    sub_category: Mapped[Optional[str]] = mapped_column(String(255))
    sector: Mapped[Optional[dict]] = mapped_column(JSONB)
    org_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    suggest_likelihood: Mapped[Optional[int]] = mapped_column(Integer)
    suggest_impact: Mapped[Optional[int]] = mapped_column(Integer)
    threat_source: Mapped[Optional[str]] = mapped_column(String(255))
    cia: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    org: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='risk_libraries')
    risk_controls: Mapped[list['RiskControls']] = relationship('RiskControls', back_populates='risk_library')
    risk_registers: Mapped[list['RiskRegisters']] = relationship('RiskRegisters', back_populates='risk_library')


class RolePermission(Base):
    __tablename__ = 'role_permission'
    __table_args__ = (
        ForeignKeyConstraint(['permission_id'], ['permissions.id'], ondelete='CASCADE', name='role_permission_permission_id_foreign'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='role_permission_role_id_foreign'),
        PrimaryKeyConstraint('id', name='role_permission_pkey'),
        UniqueConstraint('role_id', 'permission_id', name='role_permission_role_id_permission_id_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    permission_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    permission: Mapped['Permissions'] = relationship('Permissions', back_populates='role_permission')
    role: Mapped['Roles'] = relationship('Roles', back_populates='role_permission')


class SsoSetups(Base):
    __tablename__ = 'sso_setups'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='sso_setups_organization_id_foreign'),
        ForeignKeyConstraint(['sso_provider_id'], ['sso_providers.id'], ondelete='CASCADE', onupdate='CASCADE', name='sso_setups_sso_provider_id_foreign'),
        PrimaryKeyConstraint('id', name='sso_setups_pkey'),
        Index('sso_setups_organization_id_index', 'organization_id'),
        Index('sso_setups_sso_provider_id_index', 'sso_provider_id'),
        Index('sso_setups_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sso_provider_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    configuration_data: Mapped[Optional[dict]] = mapped_column(JSON)
    status: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'active'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    validated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='sso_setups')
    sso_provider: Mapped[Optional['SsoProviders']] = relationship('SsoProviders', back_populates='sso_setups')


class States(Base):
    __tablename__ = 'states'
    __table_args__ = (
        ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='CASCADE', name='states_country_id_foreign'),
        PrimaryKeyConstraint('id', name='states_pkey'),
        Index('states_country_id_index', 'country_id')
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country_id: Mapped[int] = mapped_column(Integer, nullable=False)
    flag: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    country_code: Mapped[Optional[str]] = mapped_column(String(255))
    fips_code: Mapped[Optional[str]] = mapped_column(String(255))
    iso2: Mapped[Optional[str]] = mapped_column(String(255))
    latitude: Mapped[Optional[str]] = mapped_column(String(255))
    longitude: Mapped[Optional[str]] = mapped_column(String(255))
    wikiDataId: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    country: Mapped['Countries'] = relationship('Countries', back_populates='states')


class SubCategories(Base):
    __tablename__ = 'sub_categories'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE', name='sub_categories_category_id_foreign'),
        PrimaryKeyConstraint('id', name='sub_categories_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='sub_categories')
    temp_vendors: Mapped[list['TempVendors']] = relationship('TempVendors', back_populates='sub_category')
    vendors: Mapped[list['Vendors']] = relationship('Vendors', back_populates='sub_category')


class SuggestEvidenceControlMappings(Base):
    __tablename__ = 'suggest_evidence_control_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='suggest_evidence_control_mappings_control_id_foreign'),
        ForeignKeyConstraint(['suggest_evidence_id'], ['suggest_evidence.id'], ondelete='CASCADE', name='suggest_evidence_control_mappings_suggest_evidence_id_foreign'),
        PrimaryKeyConstraint('id', name='suggest_evidence_control_mappings_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    suggest_evidence_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='suggest_evidence_control_mappings')
    suggest_evidence: Mapped['SuggestEvidence'] = relationship('SuggestEvidence', back_populates='suggest_evidence_control_mappings')


class TempPolicyUploads(Base):
    __tablename__ = 'temp_policy_uploads'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'processing'::character varying, 'completed'::character varying, 'failed'::character varying]::text[])", name='temp_policy_uploads_status_check'),
        ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL', name='temp_policy_uploads_created_by_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='temp_policy_uploads_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='temp_policy_uploads_pkey'),
        Index('temp_policy_uploads_file_hash_index', 'file_hash'),
        Index('temp_policy_uploads_org_name_version_index', 'organization_id', 'policy_name', 'policy_version')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    policy_name: Mapped[str] = mapped_column(String(255), nullable=False)
    policy_version: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    file_hash: Mapped[Optional[str]] = mapped_column(String(255))
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='temp_policy_uploads')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='temp_policy_uploads')


class TempTasks(Base):
    __tablename__ = 'temp_tasks'
    __table_args__ = (
        ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='temp_tasks_owner_id_foreign'),
        PrimaryKeyConstraint('id', name='temp_tasks_pkey'),
        Index('temp_tasks_due_date_index', 'due_date'),
        Index('temp_tasks_owner_id_index', 'owner_id'),
        Index('temp_tasks_priority_index', 'priority'),
        Index('temp_tasks_status_index', 'status'),
        Index('temp_tasks_taskable_type_taskable_id_index', 'taskable_type', 'taskable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    taskable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    taskable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[Optional[str]] = mapped_column(String(255))
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    estimated_effort: Mapped[Optional[str]] = mapped_column(String(255))
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    owner: Mapped[Optional['Users']] = relationship('Users', back_populates='temp_tasks')


class Tools(Base):
    __tablename__ = 'tools'
    __table_args__ = (
        ForeignKeyConstraint(['domain_id'], ['integration_domains.id'], name='tools_domain_id_fkey'),
        PrimaryKeyConstraint('id', name='tools_pkey'),
        UniqueConstraint('name', name='tools_name_unique'),
        Index('tools_name_index', 'name'),
        Index('tools_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'active'::character varying"))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    image_path: Mapped[Optional[str]] = mapped_column(String(255))
    configuration_keys: Mapped[Optional[dict]] = mapped_column(JSON)
    sync_type: Mapped[Optional[str]] = mapped_column(Text)
    scope: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    overview: Mapped[Optional[str]] = mapped_column(Text)
    permissions: Mapped[Optional[dict]] = mapped_column(JSON)
    resources: Mapped[Optional[dict]] = mapped_column(JSON)
    domain_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    category: Mapped[Optional[str]] = mapped_column(String(255))

    domain: Mapped[Optional['IntegrationDomains']] = relationship('IntegrationDomains', back_populates='tools')
    control_scenarios: Mapped[list['ControlScenarios']] = relationship('ControlScenarios', back_populates='tool')
    tool_integrations: Mapped[list['ToolIntegrations']] = relationship('ToolIntegrations', back_populates='tool')
    tool_evidence: Mapped[list['ToolEvidence']] = relationship('ToolEvidence', back_populates='tool')


class TrustcenterAccessRequests(Base):
    __tablename__ = 'trustcenter_access_requests'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'approved'::character varying, 'denied'::character varying]::text[])", name='trustcenter_access_requests_status_check'),
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_access_requests_company_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_access_requests_pkey'),
        Index('trustcenter_access_requests_access_token_index', 'access_token')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    requester_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    message: Mapped[Optional[str]] = mapped_column(Text)
    denial_reason: Mapped[Optional[str]] = mapped_column(Text)
    access_token: Mapped[Optional[str]] = mapped_column(String(255))
    token_expires: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_access_requests')


class TrustcenterCertifications(Base):
    __tablename__ = 'trustcenter_certifications'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['compliant'::character varying, 'in_progress'::character varying, 'not_applicable'::character varying]::text[])", name='trustcenter_certifications_status_check'),
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_certifications_company_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_certifications_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'compliant'::character varying"))
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    badge_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_certifications')


class TrustcenterCompanyControls(Base):
    __tablename__ = 'trustcenter_company_controls'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_company_controls_company_id_foreign'),
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='trustcenter_company_controls_control_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_company_controls_pkey'),
        UniqueConstraint('company_id', 'control_id', name='trustcenter_company_controls_company_id_control_id_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    is_active: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'1'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_company_controls')
    control: Mapped['Controls'] = relationship('Controls', back_populates='trustcenter_company_controls')


class TrustcenterFaqs(Base):
    __tablename__ = 'trustcenter_faqs'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_faqs_company_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_faqs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_faqs')


class TrustcenterLeadership(Base):
    __tablename__ = 'trustcenter_leadership'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_leadership_company_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_leadership_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    bio: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(500))
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_leadership')


class TrustcenterSubprocessors(Base):
    __tablename__ = 'trustcenter_subprocessors'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', name='trustcenter_subprocessors_company_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_subprocessors_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    description: Mapped[Optional[str]] = mapped_column(Text)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500))
    website: Mapped[Optional[str]] = mapped_column(String(500))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    company: Mapped['TrustcenterCompanies'] = relationship('TrustcenterCompanies', back_populates='trustcenter_subprocessors')


class TrustcenterUsers(Base):
    __tablename__ = 'trustcenter_users'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['trustcenter_companies.id'], ondelete='CASCADE', onupdate='CASCADE', name='trustcenter_users_company_id_fkey'),
        PrimaryKeyConstraint('id', name='trustcenter_users_pkey'),
        UniqueConstraint('email', name='trustcenter_users_email_unique'),
        Index('idx_users_company', 'company'),
        Index('idx_users_company_id', 'company_id'),
        Index('idx_users_deleted_at', 'deleted_at'),
        Index('idx_users_is_published', 'is_published')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    welcome_popup_seen: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    company: Mapped[Optional[str]] = mapped_column(String(255))
    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    role: Mapped[Optional[str]] = mapped_column(String(255), server_default=text("'admin'::character varying"))
    is_email_verified: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    verification_code_hash: Mapped[Optional[str]] = mapped_column(String(255))
    verification_expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    deleted_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    reset_token: Mapped[Optional[str]] = mapped_column(String(255))
    reset_token_expires_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(True, 0))
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    product: Mapped[Optional[str]] = mapped_column(String(255))

    company_: Mapped[Optional['TrustcenterCompanies']] = relationship('TrustcenterCompanies', back_populates='trustcenter_users')
    trustcenter_access_rules: Mapped['TrustcenterAccessRules'] = relationship('TrustcenterAccessRules', uselist=False, back_populates='user')
    trustcenter_activity_logs: Mapped[list['TrustcenterActivityLogs']] = relationship('TrustcenterActivityLogs', back_populates='user')
    trustcenter_documents: Mapped[list['TrustcenterDocuments']] = relationship('TrustcenterDocuments', back_populates='user')


class UserRoleOrganizations(Base):
    __tablename__ = 'user_role_organizations'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying, 'invited'::character varying, 'resent-invited'::character varying]::text[])", name='user_role_organizations_status_check'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='user_role_organizations_organization_id_foreign'),
        ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE', name='user_role_organizations_role_id_foreign'),
        PrimaryKeyConstraint('id', name='user_role_organizations_pkey'),
        UniqueConstraint('assignable_type', 'assignable_id', 'role_id', 'organization_id', name='uro_assignable_role_org_unique'),
        Index('user_role_organizations_assignable_type_assignable_id_index', 'assignable_type', 'assignable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    role_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'inactive'::character varying"))
    is_primary: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    assignable_type: Mapped[Optional[str]] = mapped_column(String(255))
    assignable_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='user_role_organizations')
    role: Mapped['Roles'] = relationship('Roles', back_populates='user_role_organizations')


class UserWebTokens(Base):
    __tablename__ = 'user_web_tokens'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='user_web_tokens_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='user_web_tokens_pkey'),
        UniqueConstraint('token', name='user_web_tokens_token_unique'),
        Index('user_web_tokens_organization_id_index', 'organization_id'),
        Index('user_web_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    tokenable_type: Mapped[Optional[str]] = mapped_column(String(255))
    tokenable_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    purpose: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='user_web_tokens')


class VendorAssessmentQuestionBanks(Base):
    __tablename__ = 'vendor_assessment_question_banks'
    __table_args__ = (
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', name='vendor_assessment_question_banks_certificate_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='vendor_assessment_question_banks_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_assessment_question_banks_pkey'),
        Index('vendor_assessment_question_banks_certificate_id_index', 'certificate_id'),
        Index('vendor_assessment_question_banks_department_index', 'department'),
        Index('vendor_assessment_question_banks_organization_id_index', 'organization_id'),
        Index('vendor_assessment_question_banks_vendor_type_index', 'vendor_type')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    certificate_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    vendor_type: Mapped[Optional[str]] = mapped_column(String(255))
    department: Mapped[Optional[str]] = mapped_column(String(255))
    question: Mapped[Optional[str]] = mapped_column(Text)
    type: Mapped[Optional[str]] = mapped_column(String(255))
    data_exposure: Mapped[Optional[str]] = mapped_column(String(255))
    weightage: Mapped[Optional[dict]] = mapped_column(JSON)
    is_attachment: Mapped[Optional[dict]] = mapped_column(JSON, server_default=text("'[]'::json"))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    certificate: Mapped[Optional['Certificates']] = relationship('Certificates', back_populates='vendor_assessment_question_banks')
    organization: Mapped[Optional['Organizations']] = relationship('Organizations', back_populates='vendor_assessment_question_banks')
    vendor_assessment_questions: Mapped[list['VendorAssessmentQuestions']] = relationship('VendorAssessmentQuestions', back_populates='vendor_assessment_question_bank')


class Vulnerabilities(Base):
    __tablename__ = 'vulnerabilities'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='vulnerabilities_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='vulnerabilities_pkey'),
        Index('assests_organization_id_index', 'organization_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    platform: Mapped[Optional[str]] = mapped_column(String(255))
    scope: Mapped[Optional[str]] = mapped_column(String(255))
    vulnerability_id: Mapped[Optional[str]] = mapped_column(String(255))
    vulnerability_name: Mapped[Optional[str]] = mapped_column(String(255))
    discovered_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    risk_score: Mapped[Optional[str]] = mapped_column(String(255))
    severity: Mapped[Optional[str]] = mapped_column(String(255))
    action_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    type: Mapped[Optional[str]] = mapped_column(String(255))
    tags: Mapped[Optional[str]] = mapped_column(String(255))
    agent_check_in: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='vulnerabilities')


class AuditClauseStatuses(Base):
    __tablename__ = 'audit_clause_statuses'
    __table_args__ = (
        ForeignKeyConstraint(['audit_id'], ['audits.id'], ondelete='CASCADE', onupdate='CASCADE', name='audit_clause_statuses_audit_id_foreign'),
        ForeignKeyConstraint(['auditor_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='audit_clause_statuses_auditor_id_foreign'),
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='CASCADE', onupdate='CASCADE', name='audit_clause_statuses_clause_id_foreign'),
        PrimaryKeyConstraint('id', name='audit_clause_statuses_pkey'),
        UniqueConstraint('audit_id', 'clause_id', name='audit_clause_unique'),
        Index('audit_clause_statuses_audit_id_index', 'audit_id'),
        Index('audit_clause_statuses_auditor_id_index', 'auditor_id'),
        Index('audit_clause_statuses_clause_id_index', 'clause_id'),
        Index('audit_clause_statuses_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    clause_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'non_compliant'::character varying"))
    auditor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    remarks: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    audit: Mapped['Audits'] = relationship('Audits', back_populates='audit_clause_statuses')
    auditor: Mapped[Optional['Users']] = relationship('Users', back_populates='audit_clause_statuses')
    clause: Mapped['Clauses'] = relationship('Clauses', back_populates='audit_clause_statuses')


class AuditMappings(Base):
    __tablename__ = 'audit_mappings'
    __table_args__ = (
        ForeignKeyConstraint(['audit_id'], ['audits.id'], ondelete='CASCADE', onupdate='CASCADE', name='audit_mappings_audit_id_foreign'),
        PrimaryKeyConstraint('id', name='audit_mappings_pkey'),
        Index('audit_mappings_audit_id_index', 'audit_id'),
        Index('audit_mappings_auditable_id_index', 'auditable_id'),
        Index('audit_mappings_auditable_type_auditable_id_index', 'auditable_type', 'auditable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    audit_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    auditable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    auditable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    audit: Mapped['Audits'] = relationship('Audits', back_populates='audit_mappings')


class ControlClauses(Base):
    __tablename__ = 'control_clauses'
    __table_args__ = (
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='control_clauses_clause_id_foreign'),
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='control_clauses_control_id_foreign'),
        PrimaryKeyConstraint('id', name='control_clauses_pkey'),
        UniqueConstraint('control_id', 'clause_id', name='control_clauses_control_id_clause_id_unique'),
        Index('control_clauses_clause_id_index', 'clause_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    clause_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    clause: Mapped['Clauses'] = relationship('Clauses', back_populates='control_clauses')
    control: Mapped['Controls'] = relationship('Controls', back_populates='control_clauses')


class ControlScenarios(Base):
    __tablename__ = 'control_scenarios'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='control_scenarios_control_id_foreign'),
        ForeignKeyConstraint(['tool_id'], ['tools.id'], ondelete='CASCADE', name='control_scenarios_tool_id_foreign'),
        PrimaryKeyConstraint('id', name='control_scenarios_pkey'),
        Index('control_scenarios_control_id_tool_id_index', 'control_id', 'tool_id'),
        Index('control_scenarios_evidence_name_index', 'evidence_name')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    tool_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    evidence_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'active'::character varying"))
    evidence_type: Mapped[Optional[str]] = mapped_column(String(50))
    action: Mapped[Optional[str]] = mapped_column(String(100))
    actions: Mapped[Optional[dict]] = mapped_column(JSON)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='control_scenarios')
    tool: Mapped['Tools'] = relationship('Tools', back_populates='control_scenarios')


class EvidenceMasters(Base):
    __tablename__ = 'evidence_masters'
    __table_args__ = (
        ForeignKeyConstraint(['integration_domain_evidence_sources_id'], ['integration_domain_evidence_sources.id'], name='evidence_masters_integration_domain_evidence_sources_id_fkey'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='SET NULL', name='fk_policy_template'),
        PrimaryKeyConstraint('id', name='evidence_masters_pkey'),
        UniqueConstraint('code', name='evidence_masters_code_unique'),
        Index('evidence_masters_category_index', 'category')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_required_evidence: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    source: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    expected_frequency: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    required_fields: Mapped[Optional[dict]] = mapped_column(JSON)
    integration_domain_evidence_sources_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    policy_template_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    integration_domain_evidence_sources: Mapped[Optional['IntegrationDomainEvidenceSources']] = relationship('IntegrationDomainEvidenceSources', back_populates='evidence_masters')
    policy_template: Mapped[Optional['PolicyTemplates']] = relationship('PolicyTemplates', back_populates='evidence_masters')
    control_evidence_master: Mapped[list['ControlEvidenceMaster']] = relationship('ControlEvidenceMaster', back_populates='evidence_master')
    tool_evidence: Mapped[list['ToolEvidence']] = relationship('ToolEvidence', back_populates='evidence_master')


class OrganizationCertificateClauses(Base):
    __tablename__ = 'organization_certificate_clauses'
    __table_args__ = (
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', name='organization_certificate_clauses_certificate_id_foreign'),
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='CASCADE', name='organization_certificate_clauses_clause_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='organization_certificate_clauses_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_certificate_clauses_pkey'),
        UniqueConstraint('organization_id', 'certificate_id', 'clause_id', name='org_cert_clause_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    certificate_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    clause_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    certificate: Mapped[Optional['Certificates']] = relationship('Certificates', back_populates='organization_certificate_clauses')
    clause: Mapped[Optional['Clauses']] = relationship('Clauses', back_populates='organization_certificate_clauses')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_certificate_clauses')


class OrganizationCertificateControls(Base):
    __tablename__ = 'organization_certificate_controls'
    __table_args__ = (
        ForeignKeyConstraint(['assigned_by'], ['users.id'], ondelete='CASCADE', name='organization_certificate_controls_assigned_by_foreign'),
        ForeignKeyConstraint(['assignee_id'], ['users.id'], ondelete='CASCADE', name='organization_certificate_controls_assignee_id_foreign'),
        ForeignKeyConstraint(['certificate_id'], ['certificates.id'], ondelete='CASCADE', name='organization_certificate_controls_certificate_id_foreign'),
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='CASCADE', name='organization_certificate_controls_clause_id_foreign'),
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='organization_certificate_controls_control_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='organization_certificate_controls_organization_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_certificate_controls_pkey'),
        Index('organization_certificate_controls_assigned_by_index', 'assigned_by'),
        Index('organization_certificate_controls_assignee_id_index', 'assignee_id'),
        Index('organization_certificate_controls_control_id_index', 'control_id'),
        Index('organization_certificate_controls_organization_id_control_id_in', 'organization_id', 'control_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    certificate_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    clause_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    assigned_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    users: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[assigned_by], back_populates='organization_certificate_controls')
    assignee: Mapped[Optional['Users']] = relationship('Users', foreign_keys=[assignee_id], back_populates='organization_certificate_controls_')
    certificate: Mapped['Certificates'] = relationship('Certificates', back_populates='organization_certificate_controls')
    clause: Mapped['Clauses'] = relationship('Clauses', back_populates='organization_certificate_controls')
    control: Mapped['Controls'] = relationship('Controls', back_populates='organization_certificate_controls')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_certificate_controls')
    organization_internal_controls: Mapped[list['OrganizationInternalControls']] = relationship('OrganizationInternalControls', back_populates='organization_control')


class OrganizationPolicyClauses(Base):
    __tablename__ = 'organization_policy_clauses'
    __table_args__ = (
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_clauses_clause_id_foreign'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_clauses_organization_id_foreign'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='CASCADE', onupdate='CASCADE', name='organization_policy_clauses_policy_template_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_policy_clauses_pkey'),
        UniqueConstraint('organization_id', 'policy_template_id', 'clause_id', name='unique_organization_policy_clause')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    policy_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    clause_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    clause: Mapped['Clauses'] = relationship('Clauses', back_populates='organization_policy_clauses')
    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_policy_clauses')
    policy_template: Mapped['PolicyTemplates'] = relationship('PolicyTemplates', back_populates='organization_policy_clauses')


class PolicyClauses(Base):
    __tablename__ = 'policy_clauses'
    __table_args__ = (
        ForeignKeyConstraint(['clause_id'], ['clauses.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='policy_clauses_clause_id_foreign'),
        ForeignKeyConstraint(['policy_template_id'], ['policy_templates.id'], ondelete='RESTRICT', onupdate='RESTRICT', name='policy_clauses_policy_template_id_foreign'),
        PrimaryKeyConstraint('id', name='policy_clauses_pkey'),
        UniqueConstraint('policy_template_id', 'clause_id', name='policy_clauses_policy_template_id_clause_id_unique'),
        Index('policy_clauses_clause_id_index', 'clause_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    policy_template_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    clause_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    clause: Mapped['Clauses'] = relationship('Clauses', back_populates='policy_clauses')
    policy_template: Mapped['PolicyTemplates'] = relationship('PolicyTemplates', back_populates='policy_clauses')


class PolicyVersions(Base):
    __tablename__ = 'policy_versions'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['draft'::character varying, 'in_review'::character varying, 'published'::character varying, 'archived'::character varying]::text[])", name='policy_versions_status_check'),
        ForeignKeyConstraint(['approved_by'], ['users.id'], ondelete='CASCADE', name='policy_versions_approved_by_foreign'),
        ForeignKeyConstraint(['org_policy_id'], ['org_policies.id'], ondelete='CASCADE', name='policy_versions_org_policy_id_foreign'),
        PrimaryKeyConstraint('id', name='policy_versions_pkey'),
        Index('policy_versions_org_policy_id_index', 'org_policy_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    org_policy_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'draft'::character varying"))
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    version: Mapped[Optional[str]] = mapped_column(String(255))
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    policy_duration: Mapped[Optional[str]] = mapped_column(String(255))
    effective_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    next_review_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    expired_at: Mapped[Optional[datetime.date]] = mapped_column(Date)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    diff_data: Mapped[Optional[dict]] = mapped_column(JSON)
    checkpoint_template: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    suggested_policy: Mapped[Optional[str]] = mapped_column(String(255))

    users: Mapped[Optional['Users']] = relationship('Users', back_populates='policy_versions')
    org_policy: Mapped['OrgPolicies'] = relationship('OrgPolicies', back_populates='policy_versions')
    policy_approvers: Mapped[list['PolicyApprovers']] = relationship('PolicyApprovers', back_populates='policy_version')
    policy_assignees: Mapped[list['PolicyAssignees']] = relationship('PolicyAssignees', back_populates='policy_version')


class RiskControls(Base):
    __tablename__ = 'risk_controls'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='risk_controls_control_id_foreign'),
        ForeignKeyConstraint(['risk_library_id'], ['risk_libraries.id'], ondelete='CASCADE', name='risk_controls_risk_library_id_foreign'),
        PrimaryKeyConstraint('id', name='risk_controls_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    risk_library_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='risk_controls')
    risk_library: Mapped['RiskLibraries'] = relationship('RiskLibraries', back_populates='risk_controls')


class RiskRegisters(Base):
    __tablename__ = 'risk_registers'
    __table_args__ = (
        CheckConstraint("ai_status::text = ANY (ARRAY['pending'::character varying, 'in_progress'::character varying, 'complete'::character varying, 'failed'::character varying]::text[])", name='risk_registers_ai_status_check'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='risk_registers_organization_id_foreign'),
        ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL', onupdate='CASCADE', name='risk_registers_owner_id_foreign'),
        ForeignKeyConstraint(['risk_library_id'], ['risk_libraries.id'], ondelete='SET NULL', onupdate='CASCADE', name='risk_registers_risk_library_id_foreign'),
        PrimaryKeyConstraint('id', name='risk_registers_pkey'),
        UniqueConstraint('organization_id', 'risk_id', name='risk_register_org_risk_id_unique'),
        Index('risk_registers_organization_id_index', 'organization_id'),
        Index('risk_registers_risk_library_id_index', 'risk_library_id'),
        Index('risk_registers_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    risk_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'open'::character varying"))
    ai_status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    risk_library_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    llm_response: Mapped[Optional[dict]] = mapped_column(JSON)
    risk_scores: Mapped[Optional[dict]] = mapped_column(JSONB)
    identified_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    tags: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='risk_registers')
    owner: Mapped[Optional['Users']] = relationship('Users', back_populates='risk_registers')
    risk_library: Mapped[Optional['RiskLibraries']] = relationship('RiskLibraries', back_populates='risk_registers')


class TempVendors(Base):
    __tablename__ = 'temp_vendors'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE', onupdate='CASCADE', name='temp_vendors_category_id_foreign'),
        ForeignKeyConstraint(['sub_category_id'], ['sub_categories.id'], ondelete='CASCADE', onupdate='CASCADE', name='temp_vendors_sub_category_id_foreign'),
        PrimaryKeyConstraint('id', name='temp_vendors_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    business_name: Mapped[Optional[str]] = mapped_column(String(255))
    poc_name: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    data_exposure: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sub_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='temp_vendors')
    sub_category: Mapped[Optional['SubCategories']] = relationship('SubCategories', back_populates='temp_vendors')


class ToolIntegrations(Base):
    __tablename__ = 'tool_integrations'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', onupdate='CASCADE', name='tool_integrations_organization_id_foreign'),
        ForeignKeyConstraint(['tool_id'], ['tools.id'], ondelete='CASCADE', onupdate='CASCADE', name='tool_integrations_tool_id_foreign'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', onupdate='CASCADE', name='tool_integrations_user_id_foreign'),
        PrimaryKeyConstraint('id', name='tool_integrations_pkey'),
        Index('tool_integrations_organization_id_index', 'organization_id'),
        Index('tool_integrations_tool_id_index', 'tool_id'),
        Index('tool_integrations_user_id_index', 'user_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    tool_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    configuration_data: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='tool_integrations')
    tool: Mapped['Tools'] = relationship('Tools', back_populates='tool_integrations')
    user: Mapped['Users'] = relationship('Users', back_populates='tool_integrations')


class TrustcenterAccessRules(Base):
    __tablename__ = 'trustcenter_access_rules'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['trustcenter_users.id'], ondelete='CASCADE', name='trustcenter_access_rules_user_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_access_rules_pkey'),
        UniqueConstraint('user_id', name='trustcenter_access_rules_user_id_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    require_email: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    domain_whitelist: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    user: Mapped['TrustcenterUsers'] = relationship('TrustcenterUsers', back_populates='trustcenter_access_rules')


class TrustcenterActivityLogs(Base):
    __tablename__ = 'trustcenter_activity_logs'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['trustcenter_users.id'], ondelete='SET NULL', name='trustcenter_activity_logs_user_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_activity_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(precision=0), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    entity_type: Mapped[Optional[str]] = mapped_column(String(100))
    entity_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    metadata_: Mapped[Optional[dict]] = mapped_column('metadata', JSON)

    user: Mapped[Optional['TrustcenterUsers']] = relationship('TrustcenterUsers', back_populates='trustcenter_activity_logs')


class TrustcenterBranding(TrustcenterUsers):
    __tablename__ = 'trustcenter_branding'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['trustcenter_users.id'], ondelete='CASCADE', name='trustcenter_branding_user_id_foreign'),
        PrimaryKeyConstraint('user_id', name='trustcenter_branding_pkey')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    logo_url: Mapped[Optional[str]] = mapped_column(Text)
    page_title: Mapped[Optional[str]] = mapped_column(Text)
    tagline: Mapped[Optional[str]] = mapped_column(String(500))
    primary_color: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))


class TrustcenterDocuments(Base):
    __tablename__ = 'trustcenter_documents'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['trustcenter_users.id'], ondelete='CASCADE', name='trustcenter_documents_user_id_foreign'),
        PrimaryKeyConstraint('id', name='trustcenter_documents_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger)
    mime_type: Mapped[Optional[str]] = mapped_column(String(100))
    title: Mapped[Optional[str]] = mapped_column(String(255))
    expiry_date: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    user: Mapped['TrustcenterUsers'] = relationship('TrustcenterUsers', back_populates='trustcenter_documents')


class Vendors(Base):
    __tablename__ = 'vendors'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE', onupdate='CASCADE', name='vendors_category_id_foreign'),
        ForeignKeyConstraint(['sub_category_id'], ['sub_categories.id'], ondelete='CASCADE', onupdate='CASCADE', name='vendors_sub_category_id_foreign'),
        PrimaryKeyConstraint('id', name='vendors_pkey'),
        Index('vendors_business_name_index', 'business_name'),
        Index('vendors_vendor_type_index', 'vendor_type')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    poc_name: Mapped[Optional[str]] = mapped_column(String(255))
    website_url: Mapped[Optional[str]] = mapped_column(String(255))
    vendor_type: Mapped[Optional[str]] = mapped_column(String(255))
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    sub_category_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='vendors')
    sub_category: Mapped[Optional['SubCategories']] = relationship('SubCategories', back_populates='vendors')
    organization_vendors: Mapped[list['OrganizationVendors']] = relationship('OrganizationVendors', back_populates='vendor')
    vendor_assessments: Mapped[list['VendorAssessments']] = relationship('VendorAssessments', back_populates='vendor')
    vendor_details: Mapped[list['VendorDetails']] = relationship('VendorDetails', back_populates='vendor')
    vendor_certificate_details: Mapped[list['VendorCertificateDetails']] = relationship('VendorCertificateDetails', back_populates='vendor')
    vendor_llm_processes: Mapped[list['VendorLlmProcesses']] = relationship('VendorLlmProcesses', back_populates='vendor')
    vendor_page_data: Mapped[list['VendorPageData']] = relationship('VendorPageData', back_populates='vendor')
    vendor_trust_centers: Mapped[list['VendorTrustCenters']] = relationship('VendorTrustCenters', back_populates='vendor')
    vendor_evidence: Mapped[list['VendorEvidence']] = relationship('VendorEvidence', back_populates='vendor')


class ControlEvidenceMaster(Base):
    __tablename__ = 'control_evidence_master'
    __table_args__ = (
        ForeignKeyConstraint(['control_id'], ['controls.id'], ondelete='CASCADE', name='control_evidence_master_control_id_foreign'),
        ForeignKeyConstraint(['evidence_master_id'], ['evidence_masters.id'], ondelete='CASCADE', name='control_evidence_master_evidence_master_id_foreign'),
        PrimaryKeyConstraint('control_id', 'evidence_master_id', name='control_evidence_master_pkey')
    )

    control_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    evidence_master_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    control: Mapped['Controls'] = relationship('Controls', back_populates='control_evidence_master')
    evidence_master: Mapped['EvidenceMasters'] = relationship('EvidenceMasters', back_populates='control_evidence_master')


class OrganizationInternalControls(Base):
    __tablename__ = 'organization_internal_controls'
    __table_args__ = (
        ForeignKeyConstraint(['internal_control_id'], ['internal_controls.id'], ondelete='CASCADE', name='organization_internal_controls_internal_control_id_foreign'),
        ForeignKeyConstraint(['organization_control_id'], ['organization_certificate_controls.id'], ondelete='CASCADE', name='organization_internal_controls_organization_control_id_foreign'),
        ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE', name='organization_internal_controls_owner_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_internal_controls_pkey'),
        UniqueConstraint('organization_control_id', 'internal_control_id', name='organization_internal_controls_organization_control_id_internal'),
        Index('organization_internal_controls_owner_id_index', 'owner_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    internal_control_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    implemented: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('false'))
    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    internal_control: Mapped['InternalControls'] = relationship('InternalControls', back_populates='organization_internal_controls')
    organization_control: Mapped['OrganizationCertificateControls'] = relationship('OrganizationCertificateControls', back_populates='organization_internal_controls')
    owner: Mapped[Optional['Users']] = relationship('Users', back_populates='organization_internal_controls')


class OrganizationVendors(Base):
    __tablename__ = 'organization_vendors'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['invited'::character varying, 'resent-invited'::character varying, 'active'::character varying]::text[])", name='organization_vendors_status_check'),
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='organization_vendors_organization_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='organization_vendors_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='organization_vendors_pkey'),
        UniqueConstraint('organization_id', 'business_name', name='organization_vendors_organization_id_business_name_unique'),
        UniqueConstraint('organization_id', 'email', name='organization_vendors_organization_id_email_unique'),
        UniqueConstraint('organization_id', 'vendor_id', name='organization_vendors_organization_id_vendor_id_unique'),
        Index('organization_vendors_organization_id_status_index', 'organization_id', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    business_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'invited'::character varying"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='organization_vendors')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='organization_vendors')


class PolicyApprovers(Base):
    __tablename__ = 'policy_approvers'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'in_review'::character varying, 'approved'::character varying, 'rejected'::character varying]::text[])", name='policy_approvers_status_check'),
        ForeignKeyConstraint(['approver_id'], ['users.id'], ondelete='CASCADE', name='policy_approvers_approver_id_foreign'),
        ForeignKeyConstraint(['policy_version_id'], ['policy_versions.id'], ondelete='CASCADE', name='policy_approvers_policy_version_id_foreign'),
        PrimaryKeyConstraint('id', name='policy_approvers_pkey'),
        Index('policy_approvers_approver_id_index', 'approver_id'),
        Index('policy_approvers_policy_version_id_index', 'policy_version_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    policy_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    approver_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    condition: Mapped[Optional[str]] = mapped_column(String(255))
    reviewed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    approved_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    approver: Mapped[Optional['Users']] = relationship('Users', back_populates='policy_approvers')
    policy_version: Mapped[Optional['PolicyVersions']] = relationship('PolicyVersions', back_populates='policy_approvers')


class PolicyAssignees(Base):
    __tablename__ = 'policy_assignees'
    __table_args__ = (
        CheckConstraint("status::text = ANY (ARRAY['pending'::character varying, 'acknowledged'::character varying, 'in_review'::character varying, 'rejected'::character varying]::text[])", name='policy_assignees_status_check'),
        ForeignKeyConstraint(['policy_version_id'], ['policy_versions.id'], ondelete='CASCADE', name='policy_assignees_policy_version_id_foreign'),
        PrimaryKeyConstraint('id', name='policy_assignees_pkey'),
        Index('policy_assignees_assignee_id_index', 'assignee_id'),
        Index('policy_assignees_policy_version_id_index', 'policy_version_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    policy_version_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    assignee_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    acknowledged_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    policy_version: Mapped['PolicyVersions'] = relationship('PolicyVersions', back_populates='policy_assignees')


class ToolEvidence(Base):
    __tablename__ = 'tool_evidence'
    __table_args__ = (
        ForeignKeyConstraint(['evidence_master_id'], ['evidence_masters.id'], ondelete='CASCADE', name='tool_evidence_evidence_master_id_fkey'),
        ForeignKeyConstraint(['tool_id'], ['tools.id'], ondelete='CASCADE', name='tool_evidence_tool_id_fkey'),
        PrimaryKeyConstraint('id', name='tool_evidence_pkey'),
        Index('tool_evidence_evidence_master_id_index', 'evidence_master_id'),
        Index('tool_evidence_tool_id_index', 'tool_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    evidence_master_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    tool_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    api_endpoint: Mapped[Optional[str]] = mapped_column(String(255))

    evidence_master: Mapped['EvidenceMasters'] = relationship('EvidenceMasters', back_populates='tool_evidence')
    tool: Mapped['Tools'] = relationship('Tools', back_populates='tool_evidence')
    evidence: Mapped[list['Evidence']] = relationship('Evidence', back_populates='tool_evidence')


class VendorAssessments(Base):
    __tablename__ = 'vendor_assessments'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_assessments_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_assessments_pkey'),
        Index('vendor_assessments_severity_index', 'severity'),
        Index('vendor_assessments_status_index', 'status'),
        Index('vendor_assessments_vendor_id_index', 'vendor_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    data_exposure: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[Optional[str]] = mapped_column(String(255))
    result: Mapped[Optional[dict]] = mapped_column(JSON)
    contracts_expiry_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    last_assessment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    next_assessment_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    completed_on: Mapped[Optional[datetime.date]] = mapped_column(Date)
    page: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    llm_request: Mapped[Optional[dict]] = mapped_column(JSON)
    llm_response: Mapped[Optional[dict]] = mapped_column(JSON)
    llm_status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_assessments')
    vendor_assessment_questions: Mapped[list['VendorAssessmentQuestions']] = relationship('VendorAssessmentQuestions', back_populates='vendor_assessment')
    vendor_certificate_details: Mapped[list['VendorCertificateDetails']] = relationship('VendorCertificateDetails', back_populates='vendor_assessment')
    vendor_llm_processes: Mapped[list['VendorLlmProcesses']] = relationship('VendorLlmProcesses', back_populates='vendor_assessment')
    vendor_page_data: Mapped[list['VendorPageData']] = relationship('VendorPageData', back_populates='vendor_assessment')
    vendor_trust_centers: Mapped[list['VendorTrustCenters']] = relationship('VendorTrustCenters', back_populates='vendor_assessment')
    vendor_evidence: Mapped[list['VendorEvidence']] = relationship('VendorEvidence', back_populates='vendor_assessment')


class VendorDetails(Base):
    __tablename__ = 'vendor_details'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_details_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_details_pkey'),
        Index('vendor_details_email_index', 'email'),
        Index('vendor_details_status_index', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255))
    password: Mapped[Optional[str]] = mapped_column(String(255))
    contact_phone: Mapped[Optional[str]] = mapped_column(String(255))
    country: Mapped[Optional[str]] = mapped_column(String(255))
    country_code: Mapped[Optional[str]] = mapped_column(String(255))
    country_by: Mapped[Optional[str]] = mapped_column(String(255))
    state: Mapped[Optional[str]] = mapped_column(String(255))
    address: Mapped[Optional[str]] = mapped_column(Text)
    profile_img: Mapped[Optional[str]] = mapped_column(String(255))
    mode: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    contract_start_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    contract_end_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    contract_frequency: Mapped[Optional[str]] = mapped_column(String(255))
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    provider_id: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    website_url: Mapped[Optional[str]] = mapped_column(String(255))

    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_details')


class Evidence(Base):
    __tablename__ = 'evidence'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='evidence_organization_id_foreign'),
        ForeignKeyConstraint(['tool_evidence_id'], ['tool_evidence.id'], ondelete='SET NULL', name='evidence_tool_evidence_id_fkey'),
        PrimaryKeyConstraint('id', name='evidence_pkey'),
        Index('evidence_title_index', 'title'),
        Index('evidence_tool_evidence_id_index', 'tool_evidence_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    tool_evidence_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='evidence')
    tool_evidence: Mapped[Optional['ToolEvidence']] = relationship('ToolEvidence', back_populates='evidence')
    evidence_collection: Mapped[list['EvidenceCollection']] = relationship('EvidenceCollection', back_populates='evidence')
    evidence_collections: Mapped[list['EvidenceCollections']] = relationship('EvidenceCollections', back_populates='evidence')
    evidence_mappeds: Mapped[list['EvidenceMappeds']] = relationship('EvidenceMappeds', back_populates='evidence')


class VendorAssessmentQuestions(Base):
    __tablename__ = 'vendor_assessment_questions'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_assessment_questions_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_assessment_question_bank_id'], ['vendor_assessment_question_banks.id'], ondelete='CASCADE', name='vendor_assessment_questions_vendor_assessment_question_bank_id_'),
        PrimaryKeyConstraint('id', name='vendor_assessment_questions_pkey'),
        Index('vendor_assessment_questions_status_index', 'status'),
        Index('vendor_assessment_questions_vendor_assessment_id_index', 'vendor_assessment_id'),
        Index('vendor_assessment_questions_vendor_assessment_question_bank_id_', 'vendor_assessment_question_bank_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_assessment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_question_bank_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    answer: Mapped[Optional[dict]] = mapped_column(JSON)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)
    score: Mapped[Optional[dict]] = mapped_column(JSON)
    status: Mapped[Optional[str]] = mapped_column(String(255))
    reference: Mapped[Optional[str]] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    llm_response: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_assessment: Mapped['VendorAssessments'] = relationship('VendorAssessments', back_populates='vendor_assessment_questions')
    vendor_assessment_question_bank: Mapped['VendorAssessmentQuestionBanks'] = relationship('VendorAssessmentQuestionBanks', back_populates='vendor_assessment_questions')
    vendor_evidence: Mapped[list['VendorEvidence']] = relationship('VendorEvidence', back_populates='vendor_assessment_question')


class VendorCertificateDetails(Base):
    __tablename__ = 'vendor_certificate_details'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_certificate_details_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_certificate_details_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_certificate_details_pkey'),
        UniqueConstraint('vendor_id', 'vendor_assessment_id', name='vendor_cert_unique')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    framework: Mapped[Optional[str]] = mapped_column(String(255))
    certification_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    issued_by: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_assessment: Mapped['VendorAssessments'] = relationship('VendorAssessments', back_populates='vendor_certificate_details')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_certificate_details')


class VendorLlmProcesses(Base):
    __tablename__ = 'vendor_llm_processes'
    __table_args__ = (
        ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE', name='vendor_llm_processes_organization_id_foreign'),
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_llm_processes_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_llm_processes_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_llm_processes_pkey'),
        Index('vendor_llm_processes_llm_status_index', 'llm_status'),
        Index('vendor_llm_processes_organization_id_index', 'organization_id'),
        Index('vendor_llm_processes_vendor_assessment_id_index', 'vendor_assessment_id'),
        Index('vendor_llm_processes_vendor_id_index', 'vendor_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    llm_status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text('0'))
    selected_pages: Mapped[Optional[dict]] = mapped_column(JSON)
    llm_request: Mapped[Optional[dict]] = mapped_column(JSON)
    llm_response: Mapped[Optional[dict]] = mapped_column(JSON)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    processed_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    organization: Mapped['Organizations'] = relationship('Organizations', back_populates='vendor_llm_processes')
    vendor_assessment: Mapped['VendorAssessments'] = relationship('VendorAssessments', back_populates='vendor_llm_processes')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_llm_processes')


class VendorPageData(Base):
    __tablename__ = 'vendor_page_data'
    __table_args__ = (
        CheckConstraint("page_type::text = ANY (ARRAY['trustcenter'::character varying, 'compliance'::character varying, 'policy'::character varying]::text[])", name='vendor_page_data_page_type_check'),
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_page_data_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_page_data_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_page_data_pkey'),
        Index('vendor_page_data_page_type_index', 'page_type'),
        Index('vendor_page_data_vendor_assessment_id_index', 'vendor_assessment_id'),
        Index('vendor_page_data_vendor_id_index', 'vendor_id'),
        Index('vendor_page_data_vendor_id_vendor_assessment_id_page_type_index', 'vendor_id', 'vendor_assessment_id', 'page_type')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    page_type: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_assessment: Mapped['VendorAssessments'] = relationship('VendorAssessments', back_populates='vendor_page_data')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_page_data')
    vendor_page_documents: Mapped[list['VendorPageDocuments']] = relationship('VendorPageDocuments', back_populates='vendor_page_data')


class VendorTrustCenters(Base):
    __tablename__ = 'vendor_trust_centers'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_trust_centers_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_trust_centers_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_trust_centers_pkey'),
        Index('vendor_trust_centers_vendor_assessment_id_index', 'vendor_assessment_id'),
        Index('vendor_trust_centers_vendor_id_index', 'vendor_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    vendor_assessment_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    provider: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_assessment: Mapped[Optional['VendorAssessments']] = relationship('VendorAssessments', back_populates='vendor_trust_centers')
    vendor: Mapped[Optional['Vendors']] = relationship('Vendors', back_populates='vendor_trust_centers')


class EvidenceCollection(Base):
    __tablename__ = 'evidence_collection'
    __table_args__ = (
        ForeignKeyConstraint(['evidence_id'], ['evidence.id'], ondelete='CASCADE', name='evidence_collection_evidence_id_fkey'),
        PrimaryKeyConstraint('id', name='evidence_collection_pkey'),
        Index('ix_evidence_collection_evidence_id', 'evidence_id'),
        Index('ix_evidence_collection_organization_id', 'organization_id'),
        Index('ix_evidence_collection_tool_id', 'tool_id'),
        Index('ix_evidence_collection_user_id', 'user_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    organization_id: Mapped[str] = mapped_column(String(36), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    tool_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    evidence_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    detail: Mapped[Optional[dict]] = mapped_column(JSON)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    completed_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))

    evidence: Mapped[Optional['Evidence']] = relationship('Evidence', back_populates='evidence_collection')


class EvidenceCollections(Base):
    __tablename__ = 'evidence_collections'
    __table_args__ = (
        CheckConstraint("evidence_from::text = ANY (ARRAY['document'::character varying, 'link'::character varying, 'integration'::character varying, 'tool'::character varying]::text[])", name='evidence_collections_evidence_from_check'),
        ForeignKeyConstraint(['evidence_id'], ['evidence.id'], ondelete='CASCADE', name='evidence_collections_evidence_id_foreign'),
        PrimaryKeyConstraint('id', name='evidence_collections_pkey'),
        Index('evidence_collection_evidence_id_index', 'evidence_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    evidence_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    evidence_from: Mapped[Optional[str]] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    tool_evidence: Mapped[Optional[dict]] = mapped_column(JSONB)
    updated_by: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    evidence: Mapped['Evidence'] = relationship('Evidence', back_populates='evidence_collections')
    tasks: Mapped[list['Tasks']] = relationship('Tasks', back_populates='evidence_collection')


class EvidenceMappeds(Base):
    __tablename__ = 'evidence_mappeds'
    __table_args__ = (
        ForeignKeyConstraint(['evidence_id'], ['evidence.id'], ondelete='CASCADE', name='evidence_mappeds_evidence_id_foreign'),
        PrimaryKeyConstraint('id', name='evidence_mappeds_pkey'),
        Index('evidence_mappeds_evidenceable_id_index', 'evidenceable_id'),
        Index('evidence_mappeds_evidenceable_type_evidenceable_id_index', 'evidenceable_type', 'evidenceable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    evidence_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    evidenceable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    evidenceable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    mapped_by: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    evidence: Mapped['Evidence'] = relationship('Evidence', back_populates='evidence_mappeds')


class VendorEvidence(Base):
    __tablename__ = 'vendor_evidence'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_assessment_id'], ['vendor_assessments.id'], ondelete='CASCADE', name='vendor_evidence_vendor_assessment_id_foreign'),
        ForeignKeyConstraint(['vendor_assessment_question_id'], ['vendor_assessment_questions.id'], ondelete='CASCADE', name='vendor_evidence_vendor_assessment_question_id_foreign'),
        ForeignKeyConstraint(['vendor_id'], ['vendors.id'], ondelete='CASCADE', name='vendor_evidence_vendor_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_evidence_pkey'),
        Index('vendor_evidence_name_index', 'name')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    vendor_assessment_question_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    path: Mapped[Optional[str]] = mapped_column(String(255))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_assessment: Mapped['VendorAssessments'] = relationship('VendorAssessments', back_populates='vendor_evidence')
    vendor_assessment_question: Mapped['VendorAssessmentQuestions'] = relationship('VendorAssessmentQuestions', back_populates='vendor_evidence')
    vendor: Mapped['Vendors'] = relationship('Vendors', back_populates='vendor_evidence')


class VendorPageDocuments(Base):
    __tablename__ = 'vendor_page_documents'
    __table_args__ = (
        ForeignKeyConstraint(['vendor_page_data_id'], ['vendor_page_data.id'], ondelete='CASCADE', name='vendor_page_documents_vendor_page_data_id_foreign'),
        PrimaryKeyConstraint('id', name='vendor_page_documents_pkey'),
        Index('vendor_page_documents_vendor_page_data_id_index', 'vendor_page_data_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    vendor_page_data_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    vendor_page_data: Mapped['VendorPageData'] = relationship('VendorPageData', back_populates='vendor_page_documents')


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = (
        ForeignKeyConstraint(['evidence_collection_id'], ['evidence_collections.id'], ondelete='SET NULL', onupdate='CASCADE', name='tasks_evidence_collection_id_foreign'),
        PrimaryKeyConstraint('id', name='tasks_pkey'),
        Index('tasks_created_by_id_type_created_by_id_id_index', 'created_by_id_type', 'created_by_id_id'),
        Index('tasks_due_date_index', 'due_date'),
        Index('tasks_evidence_collection_id_index', 'evidence_collection_id'),
        Index('tasks_owner_id_type_owner_id_id_index', 'owner_id_type', 'owner_id_id'),
        Index('tasks_priority_index', 'priority'),
        Index('tasks_status_index', 'status'),
        Index('tasks_taskable_type_taskable_id_index', 'taskable_type', 'taskable_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    taskable_type: Mapped[str] = mapped_column(String(255), nullable=False)
    taskable_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    owner_id_type: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("'pending'::character varying"))
    created_by_id_type: Mapped[str] = mapped_column(String(255), nullable=False)
    created_by_id_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[Optional[str]] = mapped_column(String(255))
    estimated_effort: Mapped[Optional[str]] = mapped_column(String(255))
    due_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    category: Mapped[Optional[str]] = mapped_column(String(255))
    subcategory: Mapped[Optional[str]] = mapped_column(String(255))
    evidence_collection_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    evidence_collection: Mapped[Optional['EvidenceCollections']] = relationship('EvidenceCollections', back_populates='tasks')
    task_attachments: Mapped[list['TaskAttachments']] = relationship('TaskAttachments', back_populates='task')


class TaskAttachments(Base):
    __tablename__ = 'task_attachments'
    __table_args__ = (
        ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE', onupdate='CASCADE', name='task_attachments_task_id_foreign'),
        PrimaryKeyConstraint('id', name='task_attachments_pkey'),
        Index('task_attachments_task_id_index', 'task_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    task_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    source: Mapped[Optional[str]] = mapped_column(String(255))
    file_type: Mapped[Optional[str]] = mapped_column(String(255))
    updated_by: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(TIMESTAMP(precision=0))

    task: Mapped['Tasks'] = relationship('Tasks', back_populates='task_attachments')
