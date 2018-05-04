SELECT a.nct_id,
         conditions,
         interventions,
         number_of_facilities,
         has_us_facility,
         country,
         number_of_sponsors,
         number_of_sae_subjects,
         enrollment
FROM 
    (SELECT studies.nct_id,
         browse_conditions.downcase_mesh_term AS conditions,
         browse_interventions.downcase_mesh_term AS interventions,
         number_of_facilities,
         has_us_facility,
         countries.name AS country,
         number_of_sae_subjects,
         enrollment
    FROM studies
    JOIN calculated_values
        ON studies.nct_id=calculated_values.nct_id
    JOIN browse_interventions
        ON studies.nct_id=browse_interventions.nct_id
    JOIN browse_conditions
        ON studies.nct_id=browse_conditions.nct_id
    JOIN countries
        ON studies.nct_id=countries.nct_id
    WHERE number_of_sae_subjects IS NOT NULL
            AND countries.name!=''
            AND number_of_facilities IS NOT NULL
            AND has_us_facility!=''
            AND enrollment IS NOT NULL) a
INNER JOIN 
    (SELECT nct_id,
         count(nct_id) AS number_of_sponsors
    FROM sponsors
    GROUP BY  nct_id) b
    ON a.nct_id = b.nct_id;
