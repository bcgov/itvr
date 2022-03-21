/* eslint-disable react/jsx-indent */
import React, { useState } from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Box from '@mui/material/Box';

const ApplicationConsent = (props) => {
  const commonStyles = {
    bgcolor: 'background.paper',
    width: '100%',
    height: 500,
    overflowY: 'scroll'
  };
  const emliAddress = (
    <div className="emli-address">
      Ministry of Energy, Mines and Low Carbon Innovation
      <br />
      Clean Transportation Branch
      <br />
      PO BOX 9314 Stn Prov Govt
      <br />
      Victoria, BC
      <br />
      V8W 9N1
      <br />
    </div>
  );
  const consentPersonalInformation = (
    <div className="consent-list">
      <ol>
        <li>
          I hereby consent to the:
          <ol type="a">
            <li>use;</li>
            <li>disclosure to the Canada Revenue Agency and</li>
            <li>
              storage and access in Canada by the government of British Columbia
              by the Ministry of Energy, Mines and Low Carbon Innovation and its
              independent contractors, subcontractors, service providers,
              licensees, and assignees of my personal information supplied
              herein (the “Personal Information”).
            </li>
          </ol>
        </li>
        <li>I confirm the information I have supplied is true and complete.</li>
        <li>
          I certify, by submitting this application form, that all information
          is complete and accurate, and it is my responsibility to advise the
          Ministry of Energy, Mines and Low Carbon Innovation immediately if
          there is any change in the information in this form that may affect my
          eligibility under the CleanBC Go Electric Vehicle Rebate program.
        </li>
        <li>
          Any misinformation or errors in information can result in the Ministry
          of Energy, Mines and Low Carbon Innovation and any other ministry,
          agency or contractor of the Government of British Columbia requiring
          the return of the money I and my spouse (if applicable) received,
          which will be due and payable upon demand.
        </li>
        <li>
          I understand that the personal information I provide on this form is
          collected under s. 26(c) of the Freedom of Information and Protection
          of Privacy Act for the purpose of assessing my eligibility for, and to
          administer the CleanBC Go Electric Vehicle Rebate program, and
          information may also be collected and disclosed in accordance with s.
          27(1)(b) and 33(2)(c) of the Freedom of Information and Protection of
          Privacy Act.
        </li>
        <li>
          I agree that any information about me that is or has been obtained by
          the British Columbia Ministry of Energy, Mines and Low Carbon
          Innovation for purposes of administering the CleanBC Go Electric
          Vehicle Rebate Program, or any information that is prepared from that
          information, may be provided to and used by any person employed in the
          service of, occupying a position of responsibility in the service of,
          or engaged by or on behalf of, the government of British Columbia for
          the purposes of research, the formulation or evaluation of fiscal
          policy, processing this application, verifying or investigating
          information related to this application, and/or the collection of any
          money that becomes due by me to the government of British Columbia as
          a result of incorrect information provided in this application. I also
          agree that information about me that I provide to any person referred
          to above may be provided to any other person referred to above and
          used for these same purposes. Finally, I agree that information about
          me that I provide to the CleanBC Go Electric Vehicle Rebate program
          may be disclosed to my spouse if applicable.
        </li>
        <li>
          If applying for a household rebate I also consent to the disclosure of
          my personal information to my spouse who is applying. This includes
          but is not limited to income information that has been used to
          calculate the rebate amount.
        </li>
        <li>
          I consent to the verification of information provided regarding this
          application, or any subsequently provided information.
        </li>
        <li>
          This consent is effective on the date by which I indicate that I
          understand and agree to the statements and will not expire unless
          revoked by me in writing to the contact listed below. My consent and
          personal information may be retained for up to five years.
        </li>
      </ol>
      {emliAddress}
    </div>
  );
  const consentTax = (
    <div className="consent-list">
      <ol>
        <li>
          I hereby consent to the disclosure of information from my income tax
          records and other taxpayer information by the Canada Revenue Agency to
          an official of the Ministry of Energy, Mines and Low Carbon
          Innovation. The information disclosed will be relevant to, and used
          solely for the purpose of, determining and verifying eligibility for
          the CleanBC Go Electric Passenger Vehicle Rebate program and for
          determining the amount of the rebate I/we are to receive under the
          program. The information disclosed by the Canada Revenue Agency to the
          Ministry of Energy, Mines and Low Carbon Innovation will be protected
          from unauthorized use or disclosure and will only be used, disclosed
          and retained in accordance with the Freedom of Information and
          Protection of Privacy Act.
        </li>
        <li>
          I also permit the Ministry of Energy, Mines and Low Carbon Innovation
          to collect information from my income tax records, and other tax
          information from the Canada Revenue Agency, instead of directly from
          me.
        </li>
        <li>
          I also consent to the disclosure of my first and last name, birth
          date, and Social Insurance Number by the Ministry of Energy, Mines and
          Low Carbon Innovation to the Canada Revenue Agency. This information
          will be used by the Canada Revenue Agency to identify the taxpayer
          information to be disclosed to the Ministry of Energy, Mines and Low
          Carbon Innovation.
        </li>
        <li>
          I further permit the Ministry of Energy, Mines and Low Carbon
          Innovation to display my income tax information from the Canada
          Revenue Agency on the electronic online portal for the purpose of
          describing how financial eligibility was calculated.
        </li>
        <li>
          This consent permits the Canada Revenue Agency to disclose information
          from my tax records and other taxpayer information from the most
          recent tax year to the year of signature of this consent.
        </li>
        This consent is effective on the date by which I indicate that I
        understand and agree to the statements and will not expire unless
        revoked by me in writing to the contact listed below.
      </ol>
      {emliAddress}
    </div>
  );
  const [consent, setConsent] = useState([
    {
      title:
        'Consent to Disclosure and Storage of, and Access to, Personal Information',
      description: consentPersonalInformation,
      type: 'personal',
      checked: false
    },
    {
      title: 'Consent to Disclosure of information from income tax records',
      type: 'tax',
      description: consentTax,
      checked: false
    }
  ]);

  const label =
    'I understand that by submitting this application form it means:';

  const handleCheckboxChange = (event, index) => {
    let consentChecked = [...consent];
    consentChecked[index].checked = event.target.checked;
    setConsent(consentChecked);
  };

  return (
    <>
      {consent.map((consentInfo, index) => {
        return (
          <div key={index}>
            <h3>{consentInfo.title}</h3>
            <p>
              You must read the following statements and use the checkbox to
              indicate that you understand and agree.
            </p>
            {consentInfo.type === 'tax' && (
              <p>
                You and your spouse (if applicable) are required to provide
                consent that allows the Ministry of Energy, Mines and Low Carbon
                Innovation to access and review tax information related to line
                15000 ‘gross income’ of your Notice of Assessment from the
                Canada Revenue Agency for the most recent tax year for your
                application to the CleanBC Go Electric Vehicle Rebate program.
              </p>
            )}
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    onChange={(e) => {
                      handleCheckboxChange(e, index);
                    }}
                  />
                }
                className="label"
                label={label}
              />
            </FormGroup>
            <div className="box-container">
              <Box sx={{ ...commonStyles }}>{consentInfo.description}</Box>
            </div>
          </div>
        );
      })}
    </>
  );
};

export default ApplicationConsent;
