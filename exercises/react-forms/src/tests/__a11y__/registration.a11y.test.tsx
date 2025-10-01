import axe from 'axe-core';
import { render } from '@testing-library/react';
import { RegistrationForm } from '../../components/forms/RegistrationForm';

describe('RegistrationForm accessibility', () => {
  test('has no detectable axe violations', async () => {
    const { container } = render(<RegistrationForm />);
    const results = await axe.run(container, {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa'],
      },
    });

    expect(results.violations).toHaveLength(0);
  });
});
