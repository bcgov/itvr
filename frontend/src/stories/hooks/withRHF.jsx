import { action } from '@storybook/addon-actions';
import { defaultValues } from '../../components/Form';
import { FormProvider, useForm } from 'react-hook-form';

const StorybookFormProvider = ({ children }) => {
  const methods = useForm({ defaultValues });
  return (
    <FormProvider {...methods}>
      <form
        onSubmit={methods.handleSubmit(action('[React Hooks Form] Submit'))}
      >
        {children}
      </form>
    </FormProvider>
  );
};

export const withRHF = (showSubmitButton) => (Story) =>
  (
    <StorybookFormProvider>
      <Story />
      {showSubmitButton && <button type="submit">Submit</button>}
    </StorybookFormProvider>
  );
