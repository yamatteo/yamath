import React from 'react'
import { Button, Link, Navbar } from '../generic_components.jsx'
import { api } from '../fetch.jsx'

export function RandomQuestionPage(props) {
  const app = props.app
  const arraySetState = app.arraySetState
  const node_serial = app.state.pageState.node_serial
  const question = (() => {
    try {
      return props.app.state.pageState.question
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
          <div className="col-sm-5 col-12">
            <Button
              text="Mostra soluzione"
              className="btn btn-warning w-100"
              lambda={() => arraySetState(['pageState', 'showSolution'], true)}
            />
          </div>
          <div className="col-sm-2" />
          <div className="col-sm-5 col-12">
            <Button
              text="Altro simile"
              className="btn btn-success w-100"
              lambda={() =>
                arraySetState(['pageState', 'showSolution'], false).then(state =>
                  arraySetState(['pageState', 'question'], null, state),
                )
              }
            />
          </div>
        </div>
        <div className="row">
          <div className="col-12">{app.state.pageState.showSolution && <p>{question.solution}</p>}</div>
        </div>
      </div>
    )
  } else {
    const node_questions = (() => {
      try {
        return app.state.nodes[node_serial].questions
      } catch (e) {
        return undefined
      }
    })()
    if (node_questions) {
      arraySetState(['pageState', 'question'], node_questions[Math.floor(Math.random() * node_questions.length)])
    } else {
      api('/api/node_questions', { node_serial: node_serial }).then(res =>
        arraySetState(['nodes', node_serial, 'questions'], res.questions),
      )
    }
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
