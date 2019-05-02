from Stepper import stepper

#stepper variables
#[stepPin, directionPin, enablePin]
runStepper = stepper([25, 26, 27])

#test stepper
runStepper.step(4000, "left"); #steps, dir, speed, stayOn
runStepper.cleanGPIO