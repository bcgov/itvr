import ConsentGeneral from './ConsentGeneral';

const ConsentTax = ({ name, required, applicationType }) => {
  const date = new Date();

  const currentYear = date.getFullYear();
  const lastYear = date.getFullYear() - 1;
  const twoYearsAgo = date.getFullYear() - 2;
  const nextYear = date.getFullYear() + 1;

  // check if date falls between july 1 and dec 31
  const isBetweenJuly1AndDec31 = date.getMonth() >= 6 && date.getMonth() <= 11
  //check if date falls between january 1 and june 30
  const isBetweenJan1AndJune30 = date.getMonth() >= 0 && date.getMonth() <= 5

  const mostRecent = isBetweenJuly1AndDec31 ? lastYear : isBetweenJan1AndJune30 ? twoYearsAgo : 'Error'
  const future = isBetweenJuly1AndDec31 ? nextYear : isBetweenJan1AndJune30 ? currentYear : 'Error'
  const modified = isBetweenJuly1AndDec31 ? currentYear : isBetweenJan1AndJune30 ? lastYear : 'Error'

  const subtitle = `You are required to provide consent that allows the Ministry of Energy, Mines and Low Carbon Innovation to access and 
  review tax information related to line 15000 ‘gross income’ of your most recent Notice of Assessment from the Canada 
  Revenue Agency for your application to the CleanBC Go Electric Passenger Vehicle Rebate program. Currently your
  ${mostRecent} NOA is considered your most recent, on July 1, ${future} it will change to be your ${modified} NOA.`;

  return (
    <ConsentGeneral
      title="Consent to disclosure of information from income tax records"
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
          <li>
            This consent is effective on the date by which I indicate that I
            understand and agree to the statements and will not expire unless
            revoked by me in writing to the contact listed below.
          </li>
        </ol>
      </div>
    </ConsentGeneral>
  );
};
export default ConsentTax;
