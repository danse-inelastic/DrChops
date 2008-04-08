<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!                                   Jiao Lin
!                      California Institute of Technology
!                        (C) 2007  All Rights Reserved
!
! {LicenseText}
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->

<!DOCTYPE inventory>

<inventory>

    <component name="PharosReductionApp">

        <property name="reducer">PowderReduction</property>

        <component name="PowderReduction">

            <property name="measurementFactory">PharosMeasurement</property>

            <component name="SpeReducer">

                <component name="Idpt2Spe">

                    <component name="energy">
                        <property name="min">-50.0</property>
                        <property name="max">50.0</property>
                        <property name="step">1.0</property>
                        <property name="unit">meV</property>
                    </component>

                    <component name="phi">
                        <property name="min">5.0</property>
                        <property name="max">150.0</property>
                        <property name="step">2.0</property>
                        <property name="unit">degree</property>
                        <property name="min">2.0</property>
                    </component>

                </component>

            </component>


            <component name="Spe2Sqe">

                <component name="Q">
                    <property name="max">13.0</property>
                    <property name="step">0.1</property>
                    <property name="unit">angstrom**-1</property>
                </component>

            </component>

        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Tue Jul 17 14:30:27 2007-->

<!-- End of file -->
