import React, { Component } from 'react'
import { ClassePrima } from './classe_prima.jsx'
import { ClasseSeconda } from './classe_seconda.jsx'
import { ClasseTerza } from './classe_terza.jsx'
import { ClasseQuarta } from './classe_quarta.jsx'
import { ClasseQuinta } from './classe_quinta.jsx'
import { LoginPage } from './login.jsx'
import { QuestionPage } from './question.jsx'
import { WelcomePage } from './welcome.jsx'

export function PageSelector(props) {
  const app = props.app
  const set = props.set || (props.app && props.app.set)
  const pageName = props.pageName || (props.app && props.app.state && props.app.state.pageName)
  const dict = {
    classe_prima: <ClassePrima app={app}/>,
    classe_seconda: <ClasseSeconda app={app}/>,
    classe_terza: <ClasseTerza app={app}/>,
    classe_quarta: <ClasseQuarta app={app}/>,
    classe_quinta: <ClasseQuinta app={app}/>,
    login: <LoginPage app={app}/>,
    question: <QuestionPage app={app}/>,
    welcome: <WelcomePage set={set}/>,
  }
  try {
    if (! dict[pageName] ) { throw 'KeyError' }
    return dict[pageName]
  } catch (e) {
    return (
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <h1 class="mt-5">Errore</h1>
            <p>Per qualche motivo inspiegabile c'è stato un errore...</p>
          </div>
        </div>
      </div>
    )
  }
}
