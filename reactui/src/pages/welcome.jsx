import React from 'react'
import { Link, Navbar } from '../generic_components.jsx'

export function WelcomePage(props) {
  const set = props.set || (props.app && props.app.set)
  return (
    <div className="container">
      <div className="row">
        <div className="col-lg-12 text-left">
          <h1 className="mt-5">Benvenuto</h1>
          <p>
            Da qui puoi accedere alle singole pagine di ogni classe dove troverai esercizi suddivisi per
            tipologia.
          </p>
          <ul className="list-unstyled">
            <li>
              <Link text="Classe prima" lambda={() => set({ pageName: 'classe_prima' })} />
            </li>
            <li>
              <Link text="Classe seconda" lambda={() => set({ pageName: 'classe_seconda' })} />
            </li>
            <li>
              <Link text="Classe terza" lambda={() => set({ pageName: 'classe_terza' })} />
            </li>
            <li>
              <Link text="Classe quarta" lambda={() => set({ pageName: 'classe_quarta' })} />
            </li>
            <li>
              <Link text="Classe quinta" lambda={() => set({ pageName: 'classe_quinta' })} />
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
};