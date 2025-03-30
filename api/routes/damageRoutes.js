const express = require('express');
const router = express.Router();
const damageController = require('../controllers/damageController');
const auth = require('../middleware/auth');

router.get('/damagedata', auth.authenticate,damageController.damageData);
router.post('/saveAssessment',auth.authenticate,damageController.saveAssessment);
router.post('/saveComponent',auth.authenticate,damageController.saveComponent);


module.exports = router;