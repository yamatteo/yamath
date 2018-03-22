import React, { Component } from 'react'
import { Link } from './generic_components.jsx'
import { api } from './fetch.jsx'

export function ClassNodeSection(props) {
  const app = props.app
  const state = app.state
  const path_set = app.path_set
  const node_serial = props.node_serial
  const class_node_state = (state.class_node_state && state.class_node_state[node_serial]) || {serial:node_serial, loaded:false}
  const node_loaded = class_node_state.loaded
  console.log('classnodestate', class_node_state)
  if (node_loaded) {
    const node_name = class_node_state.name
    const node_questions = class_node_state.questions
    const show_list = class_node_state.show_list
    return (
      <p>
      <span className='h4'>{ node_name }:</span> un esercizio <Link text='a caso' lambda={() => {
          path_set('pageName', 'question')
          path_set('question_page_state', {loaded_question:false, questionId: node_questions[Math.floor(Math.random() * node_questions.length)]['_id']['$oid']})
        }}/>, oppure tutta la <Link text='lista' lambda={() => {
          path_set('class_node_state/'+node_serial+'/show_list', true)
        }}/>
        {
          (show_list) && (
            <ul>
                {node_questions.map(question => (
                  <li key={question.serial}><Link text={question.serial} lambda={() => path_set('question_page_state', {loaded_question:false, questionId: question['_id']['$oid']})}/></li>
                ))}
            </ul>
          )
        }
      </p>
    )
  } else {
    api('/api/node_questions', {node_serial: node_serial}).then(res => {
      console.log('res', res);
      path_set('class_node_state/'+node_serial+'/loaded', true)
      path_set('class_node_state/'+node_serial+'/name', res.name)
      path_set('class_node_state/'+node_serial+'/questions', res.questions)})
    return <h3>...caricamento...</h3>
  }
}
