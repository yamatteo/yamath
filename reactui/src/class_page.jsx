import React, { Component } from 'react'
// import { Link, Navbar } from './generic_components.jsx'

export function classePrima(props) {
  const app = props.app
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Classe prima</h1>
          <h3>Cinque operazioni e precedenza</h3>
          <p>Ricordando le regole della precedenza, calcola il valore delle seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$ -5 \\cdot (12 - 3 + 4) - 2 \\cdot [3 - 16 : (-2 +4)]^2 $'}</li>
            <li>{'$ [-3 + (-5) \\cdot (-1)]^3 + [-4 -(1-2)]^2$'}</li>
            <li>{'$[2 \\cdot (-3)^2 + 2 \\cdot (-3) \\cdot (-2)]^2 : [2^4 - 3 \\cdot (+6)]^2$'}</li>
            <li>{'$[3 \\cdot (-1)^2 - 3 \\cdot (-3) \\cdot (-3)]^3 : [2^2 + 5 \\cdot (-2)^2]^3$'}</li>
          </ol>
          <h3>Operazioni singole con le frazioni</h3>
          <p>Esegui i calcoli proposti e semplifica il risultato.</p>
          <ol type='a'>
            <li>{'$ \\frac 12 + \\frac 32, \\quad \\quad \\frac{7}{11} + \\frac{4}{11}$'}</li>
            <li>{'$-\\frac32 + \\frac43, \\quad \\quad -\\frac{2}{3} + \\frac34$'}</li>
            <li>{'$\\frac56 - \\frac{{5}}{{12}}, \\quad \\quad 1 - \\frac32$'}</li>
            <li>{'$\\frac 1 5 - 1, \\quad \\quad 4 + \\frac32 - \\frac34$'}</li>
            <li>{'$\\frac32 \\cdot \\frac43, \\quad \\quad 6 \\cdot \\frac52$'}</li>
            <li>{'$ -\\frac65 \\cdot \\left( - \\frac43 \\right) \\quad \\quad \\frac23 \\cdot \\frac29 $'}</li>
            <li>{'$ \\frac55 \\cdot \\frac58 \\cdot \\left( - \\frac56 \\right), \\quad \\quad \\frac32 \\cdot \\left( - \\frac89 \\right) \\cdot \\frac56 $'}</li>
            <li>{'$ \\frac32 : \\frac43, \\quad \\quad - \\frac65 : \\left( - \\frac23 \\right) $'}</li>
            <li>{'$ \\frac{+3}{2} : \\frac{-3}{2}, \\quad \\quad \\frac25 : \\frac58 : \\left( - \\frac56 \\right) $'}</li>
            <li>{'$ \\left( - \\frac23 \\right)^2, \\quad \\quad \\left( \\frac12 - 1 \\right)^3 $'}</li>
            <li>{'$ \\left( - \\frac12 \\right)^3, \\quad \\quad \\left(-\\frac35 \\right)^0 $'}</li>
          </ol>
          {/* <p class="lead">Complete with pre-defined file paths and responsive navigation!</p> */}
          {/* <ul class="list-unstyled">
            <li>Bootstrap 4.0.0</li>
            <li>jQuery 3.3.0</li>
          </ul> */}
        </div>
      </div>
    </div>
  )
}

export function classeSeconda(props) {
  const app = props.app
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Classe seconda</h1>
          <h3>Cinque operazioni e precedenza</h3>
          <p>Ricordando le regole della precedenza, calcola il valore delle seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$ -5 \\cdot (12 - 3 + 4) - 2 \\cdot [3 - 16 : (-2 +4)]^2 $'}</li>
            <li>{'$ [-3 + (-5) \\cdot (-1)]^3 + [-4 -(1-2)]^2$'}</li>
            <li>{'$[2 \\cdot (-3)^2 + 2 \\cdot (-3) \\cdot (-2)]^2 : [2^4 - 3 \\cdot (+6)]^2$'}</li>
            <li>{'$[3 \\cdot (-1)^2 - 3 \\cdot (-3) \\cdot (-3)]^3 : [2^2 + 5 \\cdot (-2)^2]^3$'}</li>
          </ol>
          <h3>Operazioni singole con le frazioni</h3>
          <p>Esegui i calcoli proposti e semplifica il risultato.</p>
          <ol type='a'>
            <li>{'$ \\frac 12 + \\frac 32, \\quad \\quad \\frac{7}{11} + \\frac{4}{11}$'}</li>
            <li>{'$-\\frac32 + \\frac43, \\quad \\quad -\\frac{2}{3} + \\frac34$'}</li>
            <li>{'$\\frac56 - \\frac{{5}}{{12}}, \\quad \\quad 1 - \\frac32$'}</li>
            <li>{'$\\frac 1 5 - 1, \\quad \\quad 4 + \\frac32 - \\frac34$'}</li>
            <li>{'$\\frac32 \\cdot \\frac43, \\quad \\quad 6 \\cdot \\frac52$'}</li>
            <li>{'$ -\\frac65 \\cdot \\left( - \\frac43 \\right) \\quad \\quad \\frac23 \\cdot \\frac29 $'}</li>
            <li>{'$ \\frac55 \\cdot \\frac58 \\cdot \\left( - \\frac56 \\right), \\quad \\quad \\frac32 \\cdot \\left( - \\frac89 \\right) \\cdot \\frac56 $'}</li>
            <li>{'$ \\frac32 : \\frac43, \\quad \\quad - \\frac65 : \\left( - \\frac23 \\right) $'}</li>
            <li>{'$ \\frac{+3}{2} : \\frac{-3}{2}, \\quad \\quad \\frac25 : \\frac58 : \\left( - \\frac56 \\right) $'}</li>
            <li>{'$ \\left( - \\frac23 \\right)^2, \\quad \\quad \\left( \\frac12 - 1 \\right)^3 $'}</li>
            <li>{'$ \\left( - \\frac12 \\right)^3, \\quad \\quad \\left(-\\frac35 \\right)^0 $'}</li>
          </ol>
          <h3>Espressioni con le frazioni</h3>
          <p>Ricordando le regole della precedenza e come si svolgono i calcoli tra frazioni, semplifica le seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$\\left( \\frac23 - \\frac76 \\right) - \\left( 1 + \\frac56 \\right) : \\left(2 - \\frac13 \\right)$'}</li>
            <li>{'$\\left( \\frac53 - \\frac72 \\right) \\cdot \\frac45 + \\left[ \\left( \\frac13 - \\frac{1}{15} \\right) \\cdot \\frac52 \\right]^2$'}</li>
            <li>{'$\\frac{63}{55} \\cdot \\frac{44}{45} + \\frac{14}{75} \\cdot \\frac{15}{35} + \\frac{2}{25}\\cdot 10 - \\frac{16}{25}:\\frac{3}{5}+\\frac{1}{15}$'}</li>
            <li>{'$\\left\\{ \\left[ \\left( \\frac12 - \\frac23 \\right) : \\left(\\frac56 - \\frac{5}{12} \\right) \\cdot \\frac12 + \\frac34 \\right] : \\frac14 \\right\\} - \\frac23 \\cdot \\left(- \\frac35 \\right)$'}</li>
            <li>{'$ \\left( \\frac32 - 2 - \\frac14 \\right) - \\left( \\frac12 - \\frac54 \\right) $'}</li>
            <li>{'$ \\left( \\frac13 - 3 \\right) - \\left[ \\left( -\\frac12 + 2 \\right) + \\left( \\frac92 - 1 \\right) \\right] $'}</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export function classeTerza(props) {
  const app = props.app
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Classe terza</h1>
          <h3>Cinque operazioni e precedenza</h3>
          <p>Ricordando le regole della precedenza, calcola il valore delle seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$ -5 \\cdot (12 - 3 + 4) - 2 \\cdot [3 - 16 : (-2 +4)]^2 $'}</li>
            <li>{'$ [-3 + (-5) \\cdot (-1)]^3 + [-4 -(1-2)]^2$'}</li>
            <li>{'$[2 \\cdot (-3)^2 + 2 \\cdot (-3) \\cdot (-2)]^2 : [2^4 - 3 \\cdot (+6)]^2$'}</li>
            <li>{'$[3 \\cdot (-1)^2 - 3 \\cdot (-3) \\cdot (-3)]^3 : [2^2 + 5 \\cdot (-2)^2]^3$'}</li>
          </ol>
          <h3>Operazioni singole con le frazioni</h3>
          <p>Esegui i calcoli proposti e semplifica il risultato.</p>
          <ol type='a'>
            <li>{'$ \\frac 12 + \\frac 32, \\quad \\quad \\frac{7}{11} + \\frac{4}{11}$'}</li>
            <li>{'$-\\frac32 + \\frac43, \\quad \\quad -\\frac{2}{3} + \\frac34$'}</li>
            <li>{'$\\frac56 - \\frac{{5}}{{12}}, \\quad \\quad 1 - \\frac32$'}</li>
            <li>{'$\\frac 1 5 - 1, \\quad \\quad 4 + \\frac32 - \\frac34$'}</li>
            <li>{'$\\frac32 \\cdot \\frac43, \\quad \\quad 6 \\cdot \\frac52$'}</li>
            <li>{'$ -\\frac65 \\cdot \\left( - \\frac43 \\right) \\quad \\quad \\frac23 \\cdot \\frac29 $'}</li>
            <li>{'$ \\frac55 \\cdot \\frac58 \\cdot \\left( - \\frac56 \\right), \\quad \\quad \\frac32 \\cdot \\left( - \\frac89 \\right) \\cdot \\frac56 $'}</li>
            <li>{'$ \\frac32 : \\frac43, \\quad \\quad - \\frac65 : \\left( - \\frac23 \\right) $'}</li>
            <li>{'$ \\frac{+3}{2} : \\frac{-3}{2}, \\quad \\quad \\frac25 : \\frac58 : \\left( - \\frac56 \\right) $'}</li>
            <li>{'$ \\left( - \\frac23 \\right)^2, \\quad \\quad \\left( \\frac12 - 1 \\right)^3 $'}</li>
            <li>{'$ \\left( - \\frac12 \\right)^3, \\quad \\quad \\left(-\\frac35 \\right)^0 $'}</li>
          </ol>
          <h3>Espressioni con le frazioni</h3>
          <p>Ricordando le regole della precedenza e come si svolgono i calcoli tra frazioni, semplifica le seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$\\left( \\frac23 - \\frac76 \\right) - \\left( 1 + \\frac56 \\right) : \\left(2 - \\frac13 \\right)$'}</li>
            <li>{'$\\left( \\frac53 - \\frac72 \\right) \\cdot \\frac45 + \\left[ \\left( \\frac13 - \\frac{1}{15} \\right) \\cdot \\frac52 \\right]^2$'}</li>
            <li>{'$\\frac{63}{55} \\cdot \\frac{44}{45} + \\frac{14}{75} \\cdot \\frac{15}{35} + \\frac{2}{25}\\cdot 10 - \\frac{16}{25}:\\frac{3}{5}+\\frac{1}{15}$'}</li>
            <li>{'$\\left\\{ \\left[ \\left( \\frac12 - \\frac23 \\right) : \\left(\\frac56 - \\frac{5}{12} \\right) \\cdot \\frac12 + \\frac34 \\right] : \\frac14 \\right\\} - \\frac23 \\cdot \\left(- \\frac35 \\right)$'}</li>
            <li>{'$ \\left( \\frac32 - 2 - \\frac14 \\right) - \\left( \\frac12 - \\frac54 \\right) $'}</li>
            <li>{'$ \\left( \\frac13 - 3 \\right) - \\left[ \\left( -\\frac12 + 2 \\right) + \\left( \\frac92 - 1 \\right) \\right] $'}</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export function classeQuarta(props) {
  const app = props.app
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Classe quarta</h1>
          <h3>Cinque operazioni e precedenza</h3>
          <p>Ricordando le regole della precedenza, calcola il valore delle seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$ -5 \\cdot (12 - 3 + 4) - 2 \\cdot [3 - 16 : (-2 +4)]^2 $'}</li>
            <li>{'$ [-3 + (-5) \\cdot (-1)]^3 + [-4 -(1-2)]^2$'}</li>
            <li>{'$[2 \\cdot (-3)^2 + 2 \\cdot (-3) \\cdot (-2)]^2 : [2^4 - 3 \\cdot (+6)]^2$'}</li>
            <li>{'$[3 \\cdot (-1)^2 - 3 \\cdot (-3) \\cdot (-3)]^3 : [2^2 + 5 \\cdot (-2)^2]^3$'}</li>
          </ol>
          <h3>Operazioni singole con le frazioni</h3>
          <p>Esegui i calcoli proposti e semplifica il risultato.</p>
          <ol type='a'>
            <li>{'$ \\frac 12 + \\frac 32, \\quad \\quad \\frac{7}{11} + \\frac{4}{11}$'}</li>
            <li>{'$-\\frac32 + \\frac43, \\quad \\quad -\\frac{2}{3} + \\frac34$'}</li>
            <li>{'$\\frac56 - \\frac{{5}}{{12}}, \\quad \\quad 1 - \\frac32$'}</li>
            <li>{'$\\frac 1 5 - 1, \\quad \\quad 4 + \\frac32 - \\frac34$'}</li>
            <li>{'$\\frac32 \\cdot \\frac43, \\quad \\quad 6 \\cdot \\frac52$'}</li>
            <li>{'$ -\\frac65 \\cdot \\left( - \\frac43 \\right) \\quad \\quad \\frac23 \\cdot \\frac29 $'}</li>
            <li>{'$ \\frac55 \\cdot \\frac58 \\cdot \\left( - \\frac56 \\right), \\quad \\quad \\frac32 \\cdot \\left( - \\frac89 \\right) \\cdot \\frac56 $'}</li>
            <li>{'$ \\frac32 : \\frac43, \\quad \\quad - \\frac65 : \\left( - \\frac23 \\right) $'}</li>
            <li>{'$ \\frac{+3}{2} : \\frac{-3}{2}, \\quad \\quad \\frac25 : \\frac58 : \\left( - \\frac56 \\right) $'}</li>
            <li>{'$ \\left( - \\frac23 \\right)^2, \\quad \\quad \\left( \\frac12 - 1 \\right)^3 $'}</li>
            <li>{'$ \\left( - \\frac12 \\right)^3, \\quad \\quad \\left(-\\frac35 \\right)^0 $'}</li>
          </ol>
          <h3>Espressioni con le frazioni</h3>
          <p>Ricordando le regole della precedenza e come si svolgono i calcoli tra frazioni, semplifica le seguenti espressioni.</p>
          <ol type='a'>
            <li>{'$\\left( \\frac23 - \\frac76 \\right) - \\left( 1 + \\frac56 \\right) : \\left(2 - \\frac13 \\right)$'}</li>
            <li>{'$\\left( \\frac53 - \\frac72 \\right) \\cdot \\frac45 + \\left[ \\left( \\frac13 - \\frac{1}{15} \\right) \\cdot \\frac52 \\right]^2$'}</li>
            <li>{'$\\frac{63}{55} \\cdot \\frac{44}{45} + \\frac{14}{75} \\cdot \\frac{15}{35} + \\frac{2}{25}\\cdot 10 - \\frac{16}{25}:\\frac{3}{5}+\\frac{1}{15}$'}</li>
            <li>{'$\\left\\{ \\left[ \\left( \\frac12 - \\frac23 \\right) : \\left(\\frac56 - \\frac{5}{12} \\right) \\cdot \\frac12 + \\frac34 \\right] : \\frac14 \\right\\} - \\frac23 \\cdot \\left(- \\frac35 \\right)$'}</li>
            <li>{'$ \\left( \\frac32 - 2 - \\frac14 \\right) - \\left( \\frac12 - \\frac54 \\right) $'}</li>
            <li>{'$ \\left( \\frac13 - 3 \\right) - \\left[ \\left( -\\frac12 + 2 \\right) + \\left( \\frac92 - 1 \\right) \\right] $'}</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export function classeQuinta(props) {
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
