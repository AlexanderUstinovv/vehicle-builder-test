"""added vehicle enties view

Revision ID: 5da85b415f8d
Revises: fa1b63fbbf44
Create Date: 2021-03-03 11:16:16.498078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5da85b415f8d'
down_revision = 'fa1b63fbbf44'
branch_labels = None
depends_on = None

view_ddl = """
    CREATE OR REPLACE VIEW vehicle_entries AS SELECT uuid_generate_v4() as sid,
           vehicle_name,
           vehicle_id,
           formation_name,
           formation_type,
           formation_id,
           parent_id,
           json_agg(json_build_object('feature_id', feature_id, 'feature_name', feature_name, 'functions', s_functions)) AS features
    FROM
      (SELECT vehicle_name,
              vehicle_id,
              formation_name,
              formation_id,
              formation_type,
              parent_id,
              feature_name,
              feature_id,
              json_agg(json_build_object('function_id', function_id, 'function_name', function_name, 'components', components)) AS s_functions
       FROM (SELECT vehicle_name,
              vehicle_id,
              formation_name,
              formation_id,
              formation_type,
              parent_id,
              feature_name,
              feature_id,
              function_id,
              function_name,
              json_agg(json_build_object('component_id', component_id, 'component_name', component_name)) AS components
       FROM
         (SELECT v2.id AS vehicle_id,
                 v2.name AS vehicle_name,
                 f.id AS feature_id,
                 f.name AS feature_name,
                 f2.id AS formation_id,
                 f2.name AS formation_name,
                 f2.type AS formation_type,
                 f2.parent_id AS parent_id,
                 bf.id AS function_id,
                 bf.name AS function_name,
                 c2.id AS component_id,
                 c2.name AS component_name
          FROM link_fact lf
          JOIN feature f ON lf.feature_id = f.id
          JOIN base_function bf ON lf.function_id = bf.id
          JOIN formation f2 ON lf.formation_id = f2.id
          JOIN component c2 ON lf.component_id = c2.id
          JOIN vehicle v2 ON lf.vehicle_id = v2.id) AS sub_c
       GROUP BY sub_c.vehicle_name,
                sub_c.vehicle_id,
                sub_c.formation_name,
                sub_c.formation_id,
                sub_c.formation_type,
                sub_c.parent_id,
                sub_c.feature_name,
                sub_c.feature_id,
                sub_c.function_id,
                sub_c.function_name) as aggr_comps
       GROUP BY vehicle_name,
                vehicle_id,
                formation_name,
                formation_id,
                parent_id,
                formation_type,
                feature_name,
                feature_id) AS c_comp
    GROUP BY vehicle_name,
             vehicle_id,
             formation_name,
             formation_id,
             parent_id,
             formation_type
         """

view_drop_query = "DROP VIEW IF EXISTS vehicle_entries"


def upgrade():
    op.execute(view_ddl)


def downgrade():
    op.execute(view_drop_query)
