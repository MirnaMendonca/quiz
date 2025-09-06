import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices_have_sequential_ids_starting_at_1():
    q = Question(title='q')
    q.add_choice('a')
    q.add_choice('b')
    q.add_choice('c')
    assert [c.id for c in q.choices] == [1, 2, 3]


def test_add_choice_with_empty_text_raises():
    q = Question(title='q')
    with pytest.raises(Exception):
        q.add_choice('')


def test_add_choice_with_text_over_100_chars_raises():
    q = Question(title='q')
    with pytest.raises(Exception):
        q.add_choice('x' * 101)


def test_remove_choice_by_id_deletes_choice():
    q = Question(title='q')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')
    q.remove_choice_by_id(c1.id)
    remaining_ids = [c.id for c in q.choices]
    assert remaining_ids == [c2.id]
    assert len(q.choices) == 1


def test_remove_choice_by_id_with_invalid_id_raises():
    q = Question(title='q')
    q.add_choice('a')
    with pytest.raises(Exception):
        q.remove_choice_by_id(999)


def test_remove_all_choices_clears_list_and_resets_id_generation():
    q = Question(title='q')
    q.add_choice('a')
    q.add_choice('b')
    q.remove_all_choices()
    assert q.choices == []
    c = q.add_choice('c')
    assert c.id == 1


def test_set_correct_choices_marks_specified_choices_as_correct():
    q = Question(title='q')
    c1 = q.add_choice('a')
    c2 = q.add_choice('b')
    c3 = q.add_choice('c')
    q.set_correct_choices([c2.id, c3.id])
    assert c2.is_correct is True
    assert c3.is_correct is True
    assert c1.is_correct is False


def test_set_correct_choices_with_invalid_id_raises_exception():
    q = Question(title='q')
    q.add_choice('a')
    with pytest.raises(Exception):
        q.set_correct_choices([42])


def test_correct_selected_choices_raises_when_exceeding_max_selections():
    q = Question(title='q', max_selections=1)
    c1 = q.add_choice('a', is_correct=True)
    c2 = q.add_choice('b', is_correct=False)
    with pytest.raises(Exception):
        q.correct_selected_choices([c1.id, c2.id])


def test_correct_selected_choices_returns_only_correct_in_selection_order():
    q = Question(title='q', max_selections=3)
    c1 = q.add_choice('a', is_correct=False)
    c2 = q.add_choice('b', is_correct=True)
    c3 = q.add_choice('c', is_correct=True)
    result = q.correct_selected_choices([c3.id, c1.id, c2.id])
    assert result == [c3.id, c2.id]