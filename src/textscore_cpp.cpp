#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <cctype>
#include <string>
#include <string_view>
#include <unordered_set>
#include <vector>

namespace {

std::string normalize(std::string_view input) {
  std::string out;
  out.reserve(input.size());
  for (unsigned char ch : input) {
    if (std::isalnum(ch) != 0) {
      out.push_back(static_cast<char>(std::tolower(ch)));
    } else if (std::isspace(ch) != 0) {
      if (!out.empty() && out.back() != ' ') {
        out.push_back(' ');
      }
    }
  }
  while (!out.empty() && out.front() == ' ') {
    out.erase(out.begin());
  }
  while (!out.empty() && out.back() == ' ') {
    out.pop_back();
  }
  return out;
}

std::unordered_set<std::string> char_ngrams(std::string_view text, int n) {
  std::unordered_set<std::string> grams;
  if (n <= 0 || static_cast<std::size_t>(n) > text.size()) {
    return grams;
  }
  grams.reserve(text.size());
  for (std::size_t i = 0; i + static_cast<std::size_t>(n) <= text.size(); ++i) {
    grams.emplace(text.substr(i, static_cast<std::size_t>(n)));
  }
  return grams;
}

double char_ngram_jaccard(std::string_view left, std::string_view right, int n) {
  const auto left_norm = normalize(left);
  const auto right_norm = normalize(right);
  const auto left_grams = char_ngrams(left_norm, n);
  const auto right_grams = char_ngrams(right_norm, n);

  if (left_grams.empty() && right_grams.empty()) {
    return 1.0;
  }
  if (left_grams.empty() || right_grams.empty()) {
    return 0.0;
  }

  std::size_t intersection = 0;
  for (const auto &gram : left_grams) {
    if (right_grams.find(gram) != right_grams.end()) {
      ++intersection;
    }
  }
  const std::size_t union_size = left_grams.size() + right_grams.size() - intersection;
  return union_size == 0 ? 0.0 : static_cast<double>(intersection) / static_cast<double>(union_size);
}

std::vector<std::pair<int, double>> rank_chunks(
    const std::string &query,
    const std::vector<std::string> &chunks,
    int n) {
  std::vector<std::pair<int, double>> ranked;
  ranked.reserve(chunks.size());
  for (std::size_t i = 0; i < chunks.size(); ++i) {
    ranked.emplace_back(static_cast<int>(i), char_ngram_jaccard(query, chunks[i], n));
  }
  std::sort(ranked.begin(), ranked.end(), [](const auto &a, const auto &b) {
    return a.second > b.second;
  });
  return ranked;
}

}  // namespace

PYBIND11_MODULE(_textscore_cpp, m) {
  m.doc() = "Character n-gram Jaccard similarity for chunk ranking demo";
  m.def("char_ngram_jaccard", &char_ngram_jaccard, pybind11::arg("left"),
        pybind11::arg("right"), pybind11::arg("n") = 3);
  m.def("rank_chunks", &rank_chunks, pybind11::arg("query"), pybind11::arg("chunks"),
        pybind11::arg("n") = 3);
}
