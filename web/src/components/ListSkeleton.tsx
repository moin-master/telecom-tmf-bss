// Placeholder rows while a list loads.
export function ListSkeleton({ label }: { label: string }) {
  return (
    <div className="rows" aria-busy="true" aria-label={label}>
      {[0, 1, 2].map((i) => (
        <div key={i} className="row row--skeleton" aria-hidden="true">
          <div className="skeleton__line skeleton__line--short" />
          <div className="skeleton__line" />
        </div>
      ))}
    </div>
  )
}
