# Lab 3: React TypeScript Registration Form

## Objective
Use Codex to build a production-ready registration form with React, TypeScript, and modern form handling.

## Requirements

Build a registration system that includes:

1. **Form Fields**
   - Email (validated)
   - Password (strength requirements)
   - Confirm Password (must match)
   - Username (unique check)
   - Terms acceptance (required)
   - Optional profile fields

2. **Validation**
   - Real-time field validation
   - Schema validation with Zod
   - Custom validators
   - Async username availability check
   - Password strength meter

3. **User Experience**
   - Accessible (WCAG 2.1 AA)
   - Mobile responsive
   - Loading states
   - Error messages
   - Success feedback
   - Progress indicator

4. **State Management**
   - React Hook Form for form state
   - Context API for global state
   - Local storage persistence

5. **Testing**
   - Unit tests with Jest
   - Component tests with React Testing Library
   - E2E tests with Playwright
   - Accessibility tests

6. **Performance**
   - Code splitting
   - Lazy loading
   - Optimistic updates
   - Debounced validation

## Codex Prompts Progression

### Step 1: Project Setup
```bash
codex "Create a React TypeScript project with Vite, configure ESLint, Prettier, and Tailwind CSS"
```

### Step 2: Form Schema
```bash
codex "Define Zod schemas for registration form with email, password, username, and terms validation"
```

### Step 3: Form Component
```bash
codex "Create RegistrationForm component using React Hook Form with Zod resolver and TypeScript types"
```

### Step 4: Custom Inputs
```bash
codex "Build custom input components with error states, labels, and accessibility attributes"
```

### Step 5: Password Strength
```bash
codex "Implement password strength meter with visual feedback and requirements checklist"
```

### Step 6: Async Validation
```bash
codex "Add async username availability check with debouncing and loading states"
```

### Step 7: Multi-Step Form
```bash
codex "Convert to multi-step form with progress indicator and step navigation"
```

### Step 8: State Management
```bash
codex "Implement form state persistence with Context API and local storage"
```

### Step 9: Testing Suite
```bash
codex "Create comprehensive test suite with unit tests, integration tests, and accessibility tests"
```

### Step 10: Performance Optimization
```bash
codex "Add code splitting, lazy loading, and performance optimizations"
```

## Starter Structure

```
src/
├── components/
│   ├── forms/
│   │   ├── RegistrationForm.tsx
│   │   ├── FormInput.tsx
│   │   ├── PasswordInput.tsx
│   │   └── ProgressIndicator.tsx
│   └── ui/
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Spinner.tsx
├── hooks/
│   ├── useFormPersistence.ts
│   └── useDebounce.ts
├── schemas/
│   └── registration.ts
├── services/
│   └── api.ts
├── utils/
│   └── validators.ts
└── App.tsx
```

## Technologies

- React 18
- TypeScript 5
- Vite
- React Hook Form
- Zod
- Tailwind CSS
- React Testing Library
- Playwright

## Form Features to Implement

### Basic Fields
```typescript
interface RegistrationData {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
  firstName?: string;
  lastName?: string;
  phoneNumber?: string;
  dateOfBirth?: Date;
  country?: string;
  newsletter?: boolean;
  terms: boolean;
}
```

### Validation Rules
- Email: Valid format, not disposable
- Username: 3-20 chars, alphanumeric + underscore
- Password: 8+ chars, uppercase, lowercase, number, special
- Phone: International format support
- Age: Must be 18+

### Accessibility Requirements
- Proper ARIA labels
- Keyboard navigation
- Screen reader support
- Focus management
- Error announcements
- High contrast support

## Success Criteria

- [ ] All form fields validate correctly
- [ ] Async username check works
- [ ] Password strength meter functional
- [ ] Form persists on refresh
- [ ] All tests pass (>90% coverage)
- [ ] WCAG 2.1 AA compliant
- [ ] Mobile responsive
- [ ] Performance score >90

## Advanced Challenges

1. Add OAuth integration (Google, GitHub)
2. Implement CAPTCHA verification
3. Add file upload for avatar
4. Create email verification flow
5. Add internationalization (i18n)

## Testing Commands

```bash
# Development
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Unit tests
npm run test

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e

# Accessibility audit
npm run test:a11y

# Build
npm run build
```

## Example Codex Session

```bash
# Start with comprehensive prompt
codex "Create a production-ready React TypeScript registration form with:
- React Hook Form + Zod validation
- Custom styled components with Tailwind
- Password strength meter
- Async username validation
- Multi-step form with progress
- Full test coverage
- Accessibility compliance
- Mobile responsive design
Include all best practices for performance, security, and UX"
```