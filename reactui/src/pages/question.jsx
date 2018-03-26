import React from 'react'
import { Button, Link, Navbar } from '../generic_components.jsx'
import { api } from '../fetch.jsx'

export function QuestionPage(props) {
  const set = props.set || (props.app && props.app.set)
  const app = props.app
  const arraySetState = app.arraySetState
  const path_set = app.path_set
  const question = (() => {
    try {
      return props.app.state.question_page_state.loaded_question
    } catch (e) {
      return undefined
    }
  })()
  if (question) {
    return (
      <div className="container">
        <div className="row">
          <div className="col-lg-12 text-left">
            <h1 className="mt-5">Domanda {question.serial}</h1>
            <p>{question.question}</p>
          </div>
        </div>
        <div className="row">
          <div className="col-md-3">
            <Button
              text="Mostra soluzione"
              className="btn btn-outline-warning"
              lambda={() => arraySetState(['question_page_state', 'showSolution'], true)}
            />
          </div>
          <div className="col-md-9">{app.state.question_page_state.showSolution && <p>{question.solution}</p>}</div>
        </div>
      </div>
    )
  } else {
    const question_id = app.state.question_page_state.questionId
    api('/api/question', { id: question_id })
      .then(res => arraySetState(['question_page_state', 'loaded_question'], res.question))
      .then(state => arraySetState(['question_page_state', 'showSolution'], false, state))
    return (
      <div className="container">
        <div className="row">
          <div className="col-lg-12 text-center">
            <h1 className="mt-5">...caricando...</h1>
          </div>
        </div>
      </div>
    )
  }
}
