<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! ['{LicenseText}']
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->

<!DOCTYPE inventory>

<inventory>

    <component name="MCSimReductionApp">
        <property name="typos">strict</property>
        <property name="reducer">PowderReduction</property>

        <component name="PowderReduction">
            <property name="measurementFactory">MCSimMeasurement</property>
            <facility name="SpeReducer">SpeReducer</facility>
            <property name="gui">False</property>
            <facility name="Spe2Sqe">Spe2Sqe</facility>
            <property name="outputDir">.</property>

            <component name="SpeReducer">
                <facility name="_Measurement">_Measurement</facility>
                <property name="preprocess">Preprocess_MainDataOnly</property>
                <facility name="Idpt2Spe">Idpt2Spe</facility>

                <component name="Preprocess_MainDataOnly">
                    <facility name="getMain">getMain</facility>
                    <facility name="preStep1">preStep1</facility>
                    <property name="eiSolver">Ei60</property>
                    <facility name="maskFromUser">maskFromUser</facility>

                    <component name="IncidentEnergySolver_UseElasticPeaks">
                        <property name="detectorSlice">(10,15),(), ()</property>
                        <property name="numPoints">8</property>
                    </component>


                    <component name="preStep1">
                        <property name="normalizer">nonormalization</property>
                        <property name="tibgRemover">TimeIndependentBackgroundRemover_AverageOverAllDetectors</property>
                        <property name="maskApplyer">ApplyMask</property>
                        <facility name="IdptExtractor">IdptExtractor</facility>

                        <component name="IdptExtractor">
                        </component>

                        <component name="TimeIndependentBackgroundRemover_AverageOverAllDetectors">
                            <property name="tbgMax">1590.0</property>
                            <property name="tbgMin">1550.0</property>
                        </component>


                        <component name="ApplyMask">
                        </component>

                    </component>


                    <component name="getMain">
                    </component>


                    <component name="maskFromUser">
                        <property name="excludedDetectors">[]</property>
                        <property name="excludedPixels">[]</property>
                        <property name="excludedSingles">[]</property>
                    </component>

                </component>


                <component name="_Measurement">
                </component>


                <component name="Idpt2Spe">
                    <property name="EAxis">energy</property>
                    <facility name="mask">mask</facility>
                    <property name="phiAxis">phi</property>

                    <component name="energy">
                        <property name="min">-50.0</property>
                        <property name="max">50.0</property>
                        <property name="step">1.0</property>
                        <property name="unit">meV</property>
                    </component>


                    <component name="mask">
                        <property name="excludedDetectors">[]</property>
                        <property name="excludedPixels">[]</property>
                        <property name="excludedSingles">[]</property>
                    </component>


                    <component name="phi">
                        <property name="min">2.0</property>
                        <property name="max">150.0</property>
                        <property name="step">2.0</property>
                        <property name="unit">degree</property>
                    </component>

                </component>

            </component>


            <component name="Spe2Sqe">
                <property name="QAxis">Q</property>

                <component name="Q">
                    <property name="min">0.0</property>
                    <property name="max">13.0</property>
                    <property name="step">0.1</property>
                    <property name="unit">angstrom**-1</property>
                </component>

            </component>


            <component name="MCSimMeasurement">
                <property name="mt"></property>
                <property name="mtCalib"></property>
                <property name="calib"></property>
                <property name="main">SimOutput-ARCS-Ei60-E20-Q5-tof(0.8,1.6,0.01)ms-ncount1000-buffersize100</property>
                <property name="vanadiumSampleFactory">VanadiumPlate</property>

                <component name="VanadiumPlate">
                    <property name="height">0.1*m</property>
                    <property name="width">0.05*m</property>
                    <property name="darkAngle">135*degree</property>
                    <property name="thickness">0.01*m</property>
                </component>

            </component>

        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Wed Nov  7 15:18:59 2007-->

<!-- End of file -->
