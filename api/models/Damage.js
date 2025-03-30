const pool = require('../config/db');
const express = require('express');
class Damage {

  static async findDamage() {
    const { rows } = await pool.query('SELECT * FROM public. damage_data');
    return rows;
   }

   static async insertData(req){
    const data = req.body['damagedata'];
    const damage_description = data['damage_description'];
    const damage_type = data['damage_type'];
    const severity = data['severity'];
    const damage_location = data['damage_location'],
    const images = data['image'];
    const impact_force = data['impact_force'];
    const speed = data['speed'];
   
    const {rows} = await pool.query(
      "INSERT INTO public.damage.data (damage_type, damage_description, severity,damage_location,images,impact_force,speed) VALUES ($1, $2,$3 ,$4,$5,$6,$7)",
      [damage_type, damage_description, severity,damage_location,images,impact_force,speed]);
      return rows[0];
    }

    static async updateData(req){
      const data = req.body['damagedata'];
    const damage_description = data['damage_description'];
    const damage_type = data['damage_type'];
    const severity = data['severity'];
    const damage_location = data['damage_location'],
    const images = data['image'];
    const impact_force = data['impact_force'];
    const speed = data['speed'];
    const damage_id = data['damage_id'];
      const {rows} = await pool.query(
        "UPDATE public.damage.data SET damage_type=$1, damage_description = $2, severity = $3, damage_location = %4, images = %5, impact_force = $6, speed = $6,  WHWER id = $11 )",
        [damage_type, damage_description, severity,damage_location,images,impact_force,speed]);
        return rows[0];
      }

  static async saveAssessment(req){
  //assessment_id, raw_input, processed_output, damage_categories,severity_scale, safety_risk, model_confidence, parts_cost,labor_cost, processing_metadata
   const raw_data = req.body['raw_data'];
   const assessment = JSON.parse(req.body['assessment']);
   const assessment_id = req.body['assessment_id'] ;
   const raw_input=raw_data;
   const processed_output= assessment;
   const damage_categories = assessment['damage_types'];
   const severity_scale = assessment['severity'];
   const safety_risk = assessment['safety_risk'];
   const model_confidence = assessment['confidence'];
   const parts_cost =  assessment['cost_estimate']['parts'];
   const labor_cost =  assessment['cost_estimate']['labor'];
   const processing_metadata = req.body['model'];
  console.log(assessment_id, raw_input, processed_output, damage_categories,severity_scale, safety_risk, model_confidence, parts_cost,labor_cost, processing_metadata);
   const {rows} = await pool.query('INSERT INTO public.damage_assessments ( assessment_id, raw_input, processed_output, damage_categories,severity_scale, safety_risk, model_confidence, parts_cost,labor_cost, processing_metadata) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)',
   [assessment_id, JSON.parse(raw_input), processed_output, damage_categories,severity_scale, safety_risk, model_confidence, parts_cost,labor_cost, JSON.parse(processing_metadata)]);
   return rows[0];
   return null;
}
// Save components
  
static async saveComponent(req){
  const components = JSON.parse(req.body['components']);
  const assessment_id=req.body['assessment_id'];
  try{
    components.map(async (component)=>{
      console.log(component['name']);
       await pool.query('INSERT INTO damage_components (assessment_id, component_name, condition, repair_action) VALUES ($1,$2,$3,$4)'
               ,['ad284b44-91d8-4cf2-bbb8-9c9d2b0e7591',component['name'].toString(),component['condition'].toString(),component['repair_action'].toString()]);             
 });
return {"message ":"saved data successfully"};
  }catch(e){
    return {"error":e};
  }
}
}
module.exports = Damage;