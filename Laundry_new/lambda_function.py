import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request

from laundry_scrape import get_laundry


app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def lambda_handler(event, _context):
    return ask.run_aws_lambda(event)


@ask.launch
def welcome():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


@ask.intent("AMAZON.HelpIntent")
def help():
    help_msg = render_template('help')
    return question(help_msg)


@ask.intent("AMAZON.FallbackIntent")
def fallback():
    fallback_msg = render_template('error-not-understand')
    return question(fallback_msg)


@ask.intent('AMAZON.CancelIntent')
@ask.intent("AMAZON.StopIntent")
def stop():
    goodbye_msg = render_template('goodbye')
    return statement(goodbye_msg)



@ask.intent('AnswerBuildingNameIntent', mapping={'laundrt_name': 'laundry_id'})
def answer_buildingname(buildingname):
	laundry_id = request.intent.slots.buildingname.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['id']
	session.attributes['laundry_id'] = laundry_id 
	session.attributes['laundry_name'] = laundry_name
	results = get_laundry(laundry_id)

	answer_msg = render_template('answer-results', 
        laundry=laundry_name,  
        result=results
	)
	return statement(answer_msg)


if __name__ == '__main__':
    app.run(debug=True)
