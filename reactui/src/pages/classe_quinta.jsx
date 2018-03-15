import React from 'react'

export function ClasseQuinta(props) {
  const app = props.app
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Classe quinta</h1>
          <h3>Studio di funzioni (dominio)</h3>
          <p>Stabilisci il dominio delle seguenti funzioni.</p>
          <ol type='a'>
            <li>{'$y = 3 - x^3 + \\sin(x)$'}</li>
            <li>{'$y = \\frac{5 - 2x}{4x + 3}$'}</li>
            <li>{'$y = \\frac14x + \\sqrt{8 - 5x}$'}</li>
            <li>{'$y = 12 - \\log_3\\!{\\left(4x + \\frac13\\right)}$'}</li>
            <li>{'$y = 5 + \\frac{5}{2 - x} + \\frac{3x + 1}{x^2 - 8x + 15}$'}</li>
            <li>{'$y = \\sqrt[3]{3x + 8} - \\sqrt{4x^2 + x - 3}$'}</li>
            <li>{'$y = \\log_4({3x + 2}) + \\sqrt{5 - x + \\frac14}$'}</li>
          </ol>
        </div>
      </div>
    </div>
  )
}
