-- OBJECTIVE: Identify "Free Tier" accounts that have hit PQL (Product Qualified Lead) thresholds
-- CONTEXT: We look for a rolling 7-day window of high activity in specific Harness modules.

WITH user_activity AS (
    SELECT 
        user_id,
        email,
        organization_id,
        COUNT(CASE WHEN event_type = 'deployment_success' THEN 1 END) as ci_cd_deployments,
        COUNT(CASE WHEN event_type = 'feature_flag_created' THEN 1 END) as flag_activity,
        COUNT(CASE WHEN event_type = 'cloud_cost_report_viewed' THEN 1 END) as ccm_activity,
        MAX(timestamp) as last_active
    FROM 
        harness_prod.segment_tracks
    WHERE 
        timestamp >= NOW() - INTERVAL '7 days'
    GROUP BY 
        1, 2, 3
),

account_status AS (
    SELECT 
        organization_id,
        subscription_tier,
        account_owner_id
    FROM 
        harness_prod.dim_organizations
    WHERE 
        subscription_tier = 'Free' -- Only target non-paying users
)

-- MAIN QUERY
SELECT 
    ua.user_id,
    ua.email,
    -- Determine the primary interest based on usage volume
    CASE 
        WHEN ua.ci_cd_deployments > 10 THEN 'Interest: CI/CD'
        WHEN ua.flag_activity > 5 THEN 'Interest: Feature Flags'
        WHEN ua.ccm_activity > 3 THEN 'Interest: Cloud Cost'
        ELSE 'General Interest' 
    END AS dominant_intent,
    ua.last_active
FROM 
    user_activity ua
JOIN 
    account_status acc ON ua.organization_id = acc.organization_id
WHERE 
    (ua.ci_cd_deployments >= 10 OR ua.flag_activity >= 5 OR ua.ccm_activity >= 3)
    AND ua.email NOT LIKE '%@harness.io' -- Exclude internal employees
