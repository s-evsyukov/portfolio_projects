# Data warehouse design

### Task: Design and describe the subject area.

---

#### It must meet the following characteristics:
- at least 5 entities
- at least 25 attributes (on all entities)
- at least one business process (transactional information)

#### The following methodologies should be used:
- Multidimensional modeling (Inmon, Kimball)
- Data Vault 2
- Anchor modeling

---

### Process:

#### DWH by "Kimball"

![DWH by "Kimball"](img\Kimball.png "Kimball")

- The model is based on: "Car service shop"
- Type: "Constellation",
- History: by type SCD6 (due to heterogeneous data history updates).
- Main entities:
- The task of the analysis:
   * the volume of customer payments for car repairs
   * volume of customer payments for the purchase of spare parts
   * type of repair work, time spent
   * volume of payments for the purchase of spare parts
  
 Measurement entities
   * car
   * client
   * garage
   * spare part
   * auto master
   * supplier
   * person
   * adress

 Facts entities (for showcase)	
   * repair payment
   * pepair order
   * spare parts payment
   * spare parts order

---

#### DWH by "Inmon"

![DWH by "Inmon"](img\Inmon.png "Inmon")

- The model is based on: "Seaport management"
- Type: "Constellation",
- History: by type SCD6 (due to heterogeneous data history updates).
- Analysis task:
   * chartering of vessels for cargo transportation
   * repair of vessels in the dock
   
Main entities:
   * vessel
   * vessel owner
   * crew member
   * cargo
   * cargo owner
   * sea port
   * port worker
   * pier
   * repair dock
  
Transaction entities:
   * vessel chartering
   * vessel repair

--- 

#### DWH по "Data Volt 2",

![DWH by "Data Volt2"](img\Data_volt2.png "Data Volt2")

- The model is based on: "Medical clinic management"
- Type: "Constellation"
- Analysis task:
   * patient's medical history
   * receiving a patient from a doctor
   * interaction of the doctor with the office
   * maintenance of the cabinet by auxiliary workers

Main entities "HUB":
   * medical history
   * patient
   * doctor
   * medical cabinet
   * maintenance_staff
    
Context entities "SATELLITE":
   * sign in history
   * treatment history
   * patient info
   * appointment info
   * doctor info
   * medical cabinet info
   * cabinet history info
   * maintenance staff info
   * repairing info

Transaction entities "LINK":
   * patient medical history
   * doctor appointment
   * doctor cabinet 
   * cabinet maintenance 

Simplified access entities "PIT":":
   * cabinet
    
The essence of Combined Access "BRIDGE":
   * medical_history_patient_doctor_medical_cabinet

---

#### DWH по "Anchor modeling"

![DWH by "Anchor modeling"](img\Anchor_modeling.png "Anchor modeling")

- The model is based on: "Chartering a bus management"
- Type: "Constellation"
- Analysis task: 
  * bus ride
  * payment for the trip

Main entities "ANCHOR":
  * bus
  * trip
  * payment

Attribute Entities "ATTRIBUTE":
- bus:
  * capacity
  * comfort level
  * brand
  * production year
  * trunk volume
-trip:
  * boarding location
  * passenger quntity
  * boarding time
  * destination point
  * trip end time
- payment:
  * amount
  * customer_FIO
  * full payment flg
  * payment dttm

Transaction entity TIE:
  * bus_trip
  * trip_payment
