interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  as?: React.ElementType;
}

export function Card({ as: Component = 'div', className = '', children, ...props }: CardProps) {
  return (
    <Component
      className={`rounded-lg border border-slate-100 bg-white shadow-sm ${className}`.trim()}
      {...props}
    >
      {children}
    </Component>
  );
}

interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardHeader({ className = '', children, ...props }: CardHeaderProps) {
  return (
    <div className={`border-b border-slate-100 px-6 py-4 ${className}`.trim()} {...props}>
      {children}
    </div>
  );
}

interface CardContentProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardContent({ className = '', children, ...props }: CardContentProps) {
  return (
    <div className={`px-6 py-4 ${className}`.trim()} {...props}>
      {children}
    </div>
  );
}

interface CardFooterProps extends React.HTMLAttributes<HTMLDivElement> {}

export function CardFooter({ className = '', children, ...props }: CardFooterProps) {
  return (
    <div className={`border-t border-slate-100 bg-slate-50 px-6 py-4 ${className}`.trim()} {...props}>
      {children}
    </div>
  );
}
