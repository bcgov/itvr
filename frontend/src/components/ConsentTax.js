import ConsentGeneral from './ConsentGeneral';

const ConsentTax = ({ name, required, applicationType }) => {
  const date = new Date();

  const currentYear = date.getFullYear();
  const subtitle = `You${
    applicationType !== 'individual' && ', and your spouse (if applicable)'
  } are required to provide consent that allows the Ministry of Energy, Mines and Low Carbon Innovation to access and 
review tax information related to line 15000 ‘gross income’ of your most recent Notice of Assessment from the Canada 
Revenue Agency for your application to the CleanBC Go Electric Passenger Vehicle Rebate program. Up until 
June 30, ${currentYear}  your ${
    currentYear - 2
  } NOA is considered your most recent, on July 1, ${currentYear} it will change to be your ${
    currentYear - 1
  } NOA.`;

  return (
    <ConsentGeneral
      title="Consent to Disclosure of Information from Income Tax Records"
      subtitle={subtitle}
      name={name}
      required={required}
    >
      <div className="consent-list">
        <ol>
          <li>
            I hereby consent to the disclosure of information from my income tax
            records and other taxpayer information by the Canada Revenue Agency
            to an official of the Ministry of Energy, Mines and Low Carbon
            Innovation. The information disclosed will be relevant to, and used
            solely for the purpose of, determining and verifying eligibility for
            the CleanBC Go Electric Passenger Vehicle Rebate program and for
            determining the amount of the rebate I/we are to receive under the
            program. The information disclosed by the Canada Revenue Agency to
            the Ministry of Energy, Mines and Low Carbon Innovation will be
            protected from unauthorized use or disclosure and will only be used,
            disclosed and retained in accordance with the Freedom of Information
            and Protection of Privacy Act.
          </li>
          <li>
            I also permit the Ministry of Energy, Mines and Low Carbon
            Innovation to collect information from my income tax records, and
            other tax information from the Canada Revenue Agency, instead of
            directly from me.
          </li>
          <li>
            I also consent to the disclosure of my first and last name, birth
            date, and Social Insurance Number by the Ministry of Energy, Mines
            and Low Carbon Innovation to the Canada Revenue Agency. This
            information will be used by the Canada Revenue Agency to identify
            the taxpayer information to be disclosed to the Ministry of Energy,
            Mines and Low Carbon Innovation.
          </li>
          <li>
            I further permit the Ministry of Energy, Mines and Low Carbon
            Innovation to display my income tax information from the Canada
            Revenue Agency on the electronic online portal for the purpose of
            describing how financial eligibility was calculated.
          </li>
          <li>
            This consent permits the Canada Revenue Agency to disclose
            information from my tax records and other taxpayer information from
            the most recent tax year to the year of signature of this consent.
          </li>
          This consent is effective on the date by which I indicate that I
          understand and agree to the statements and will not expire unless
          revoked by me in writing to the contact listed below.
        </ol>
      </div>
    </ConsentGeneral>
  );
};
export default ConsentTax;
