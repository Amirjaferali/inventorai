model MP01_B2
  "MP01 proof wrapper: the unchanged MSL example with every required input declared explicitly"
  extends Modelica.Electrical.Machines.Examples.ControlledDCDrives.SpeedControlledDCPM(
    driveData(
      motorData(
        VaNominal=100, IaNominal=100,
        wNominal=Modelica.Units.Conversions.from_rpm(1425),
        Ra=0.05, TaRef=293.15, alpha20a=0, TaNominal=293.15, La=0.0015,
        Jr=0.15, Js=0.15,
        frictionParameters(PRef=0), coreParameters(PRef=0),
        strayLoadParameters(PRef=0), brushParameters(V=0)),
      JL=0.15, fS=2000),
    armatureInverter(useIdealInverter=true),
    loadTorque(stepTorque=-1.6*driveData.tauNominal,
               startTime=0.8),
    step(startTime=0.2));
end MP01_B2;
