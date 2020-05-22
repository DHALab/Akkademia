from pathlib import Path
from data import dump_object_to_file, load_object_from_file, compute_accuracy
from build_data import preprocess
from hmm import hmm_train, hmm_preprocess, hmm_viterbi
from memm import memm_train, build_extra_decoding_arguments, memm_greedy
from BiLSTM import prepare1, prepare2, BiLSTM_predict
from allennlp.predictors import SentenceTaggerPredictor


def hmm_train_and_store():
    """
    Trains HMM model and stores all the data needed for using HMM
    :return: nothing, stores everything in hmm_model.pkl
    """
    train_texts, dev_texts, test_texts, _, _, _, _ = preprocess()
    most_common_tag, possible_tags, q, e, S, total_tokens, q_bi_counts, q_uni_counts, lambda1, lambda2 = \
        hmm_train(train_texts, dev_texts)

    dump_object_to_file((most_common_tag, possible_tags, q, e, S, total_tokens, q_bi_counts, q_uni_counts, lambda1,
                         lambda2, test_texts), Path(r"../output/hmm_model.pkl"))


def hmm_train_and_test():
    """
    Trains HMM model, stores all data and print the accuracy
    :return: nothing, stores everything in hmm_model.pkl
    """
    hmm_train_and_store()

    most_common_tag, possible_tags, q, e, S, total_tokens, q_bi_counts, q_uni_counts, lambda1, lambda2, test_texts = \
        load_object_from_file(Path(r"../output/hmm_model.pkl"))
    print(compute_accuracy(test_texts, hmm_viterbi, total_tokens, q_bi_counts, q_uni_counts, q, e, S, most_common_tag,
                           possible_tags, lambda1, lambda2))


def memm_train_and_store():
    """
    Trains MEMM model and stores all the data needed for using MEMM
    :return: nothing, stores everything in memm_model.pkl
    """
    train_texts, dev_texts, test_texts, _, _, _, _ = preprocess()

    logreg, vec, idx_to_tag_dict = memm_train(train_texts, dev_texts)

    dump_object_to_file((logreg, vec, idx_to_tag_dict, test_texts),
                        Path(r"../output/memm_model.pkl"))


def memm_train_and_test():
    """
    Trains MEMM model, stores all data and print the accuracy
    :return: nothing, stores everything in memm_model.pkl
    """
    memm_train_and_store()

    logreg, vec, idx_to_tag_dict, test_texts = \
        load_object_from_file(Path("../output/memm_model.pkl"))
    print(compute_accuracy(test_texts, memm_greedy, logreg, vec, idx_to_tag_dict))


def biLSTM_train_and_store():
    """
    Trains biLSTM model and stores all the data needed for using biLSTM
    :return: nothing, stores everything in biLSTM_model.pkl
    """
    train_texts, dev_texts, test_texts, sign_to_id, _, _, id_to_tran = preprocess()

    model, vocab, train_dataset, validation_dataset, cuda_device, reader = prepare1()
    trainer, model, reader, vocab = prepare2(model, vocab, train_dataset, validation_dataset, cuda_device, reader)
    trainer.train()
    predictor = SentenceTaggerPredictor(model, dataset_reader=reader)

    dump_object_to_file((model, predictor, sign_to_id, id_to_tran, test_texts), Path(r"../output/biLSTM_model.pkl"))


def biLSTM_train_and_test():
    """
    Trains biLSTM model, stores all data and print the accuracy
    :return: nothing, stores everything in biLSTM_model.pkl
    """
    biLSTM_train_and_store()

    model, predictor, sign_to_id, id_to_tran, test_texts = load_object_from_file(Path(r"../output/biLSTM_model.pkl"))
    print(compute_accuracy(test_texts, BiLSTM_predict, model, predictor, sign_to_id, id_to_tran))


def main():
    """
    Trains biLSTM, MEMM and HMM models, stores all data and print the accuracies
    :return: nothing, stores everything in pickles
    """
    hmm_train_and_test()
    # memm_train_and_test()
    # biLSTM_train_and_test()


if __name__ == '__main__':
    main()
