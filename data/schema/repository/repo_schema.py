from __future__ import annotations
from typing import List
from pydantic import BaseModel


class Owner(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    user_view_type: str
    site_admin: bool


class Permissions(BaseModel):
    admin: bool
    maintain: bool
    push: bool
    triage: bool
    pull: bool


class SecretScanning(BaseModel):
    status: str


class SecretScanningPushProtection(BaseModel):
    status: str


class DependabotSecurityUpdates(BaseModel):
    status: str


class SecretScanningNonProviderPatterns(BaseModel):
    status: str


class SecretScanningValidityChecks(BaseModel):
    status: str


class SecurityAndAnalysis(BaseModel):
    secret_scanning: SecretScanning
    secret_scanning_push_protection: SecretScanningPushProtection
    dependabot_security_updates: DependabotSecurityUpdates
    secret_scanning_non_provider_patterns: SecretScanningNonProviderPatterns
    secret_scanning_validity_checks: SecretScanningValidityChecks


class RepoSchema(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: Owner
    html_url: str
    description: None
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: None
    size: int
    stargazers_count: int
    watchers_count: int
    language: None
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: None
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: List
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    permissions: Permissions
    temp_clone_token: str
    allow_squash_merge: bool
    allow_merge_commit: bool
    allow_rebase_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_update_branch: bool
    use_squash_pr_title_as_default: bool
    squash_merge_commit_message: str
    squash_merge_commit_title: str
    merge_commit_message: str
    merge_commit_title: str
    security_and_analysis: SecurityAndAnalysis
    network_count: int
    subscribers_count: int
