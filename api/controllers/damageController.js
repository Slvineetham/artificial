const Damage = require('../models/Damage');
const jwt = require('jsonwebtoken');
const bodyParser = require('body-parser')

exports.damageData = async (req, res) => {
  try {   
    const damage =  await Damage.findDamage();
    if (!damage) throw new Error('User not found');
    console.log("TEst",damage);
    res.status(201).json(damage);
    
  } catch (err) {
     res.status(400).json({ error: err.message });
  }
}
exports.UpdateDamageData = async (req,res)=>{
  try{
  const damage = await Damage.updateData(req);
  res.status(201).json(damage);
  }catch(err){
    res.status(400).json({error: err.message});
  }
}

exports.damageDataInsertion = async(req,res) =>{
  try{
    const damagedata = await Damage.insertData(req);
    res.status(201).json(damage);
  }catch(err){
    res.status(400).json({error:err.message});
  }
}
exports.saveAssessment = async(req,res)=>{
  const result = await Damage.saveAssessment(req);
  console.log('result',result);
  res.status(200).json({ error:'testing' });
}

exports.saveComponent = async(req,res) => {
  const result = await Damage.saveComponent(req);
console.log(result);
res.status(200).json({ error: 'testing' });
}