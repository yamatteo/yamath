import React, { Component } from 'react'
import { AllQuestionsPage } from './all_questions.jsx'
import { ClassePrima } from './classe_prima.jsx'
import { ClasseSeconda } from './classe_seconda.jsx'
import { ClasseTerza } from './classe_terza.jsx'
import { ClasseQuarta } from './classe_quarta.jsx'
import { ClasseQuinta } from './classe_quinta.jsx'
import { LoginPage } from './login.jsx'
import { QuestionPage } from './question.jsx'
import { RandomQuestionPage } from './random_question.jsx'
import { WelcomePage } from './welcome.jsx'

export function PageSelector(props) {
  const app = props.app
  const arraySetState = app.arraySetState
  const pageName = (() => {
    try {
      return app.state.pageState.pageName
    } catch (e) {
      alert('Deprecated pageName!')
      return props.pageName || (props.app && props.app.state && props.app.state.pageName)
    }
  })();
  const dict = {
    all_questions: <AllQuestionsPage app={app}/>,
    classe_prima: <ClassePrima app={app}/>,
    classe_seconda: <ClasseSeconda app={app}/>,
    classe_terza: <ClasseTerza app={app}/>,
    classe_quarta: <ClasseQuarta app={app}/>,
    classe_quinta: <ClasseQuinta app={app}/>,
    login: <LoginPage app={app}/>,
    question: <QuestionPage app={app}/>,
    random_question: <RandomQuestionPage app={app}/>,
    welcome: <WelcomePage app={app}/>,
  }
  try {
    if (! dict[pageName] ) { throw 'KeyError' }
    return dict[pageName]
  } catch (e) {
    return (
      <div className="container">
        <div className="row">
          <div className="col-lg-12">
            <h1 className="mt-5">Errore</h1>
            <p>La pagina richiesta non può essere visualizzata. Contatta l'autore.</p>
          </div>
        </div>
      </div>
    )
  }
}
