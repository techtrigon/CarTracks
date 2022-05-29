from django.db import models

class car(models.Model):
   Make = models.CharField(max_length=60,blank=True,null=True)
   Model = models.CharField(max_length=60)
   Variant= models.CharField(max_length=100)
   Price  = models.FloatField()       
   Displacement = models.CharField(max_length=60,blank=True,null=True)
   Sales2022= models.FloatField()
   Sales2021= models.FloatField()
   Highest_sales_state= models.CharField(max_length=100)
   Color	= models.CharField(max_length=60)
   Cylinders= models.IntegerField(blank=True,null=True)
   Emission_Norm	= models.CharField(max_length=40,blank=True,null=True)
   Fuel_Tank_Capacity_ltr= models.FloatField()
   Fuel_Type= models.CharField(max_length=100)
   Body_Type= models.CharField(max_length=60)
   Doors= models.IntegerField()
   Mileage= models.CharField(max_length=100,blank=True,null=True)
   Gears= models.IntegerField(blank=True,null=True)
   Ground_Clearance= models.CharField(max_length=100,blank=True,null=True)
   Front_Brakes= models.CharField(max_length=100,blank=True,null=True)
   Rear_Brakes= models.CharField(max_length=100,blank=True,null=True)
   Front_Suspension= models.CharField(max_length=100,blank=True,null=True)
   Rear_Suspension	= models.CharField(max_length=100,blank=True,null=True)
   Front_Tyre_Rim	= models.CharField(max_length=100,blank=True,null=True)
   Rear_Tyre_Rim	= models.CharField(max_length=100,blank=True,null=True)
   Power_Steering	= models.CharField(max_length=100,blank=True,null=True)
   Power_Windows = models.CharField(max_length=100,blank=True,null=True)	
   Power	= models.CharField(max_length=100)
   Torque = models.CharField(max_length=100,blank=True,null=True)
   Seating_Capacity	= models.IntegerField()
   Boot_Space_ltr = models.IntegerField(blank=True,null=True)
   # Tags   = models.TextField()


   def __str__(self) :
      return self.Make +self.Model +self.Variant