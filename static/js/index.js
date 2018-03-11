"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var SearchResults = function (_React$Component) {
    _inherits(SearchResults, _React$Component);

    function SearchResults() {
        _classCallCheck(this, SearchResults);

        return _possibleConstructorReturn(this, (SearchResults.__proto__ || Object.getPrototypeOf(SearchResults)).apply(this, arguments));
    }

    _createClass(SearchResults, [{
        key: "render",
        value: function render() {
            var that = this;
            return this.props.results.map(function (item, i) {
                if (item._source) {
                    return React.createElement(
                        "li",
                        { style: { listStyleType: "none", backgroundColor: "white", color: "black" }, id: i },
                        React.createElement(
                            "article",
                            null,
                            React.createElement(
                                "h1",
                                { style: { textAlign: "start" } },
                                React.createElement(
                                    "a",
                                    { target: "_blank", href: that.props.baseUrl + '?id=' + item._id, rel: "external" },
                                    item._source.title + " " + item._source.year
                                )
                            ),
                            React.createElement(
                                "p",
                                { style: { display: "flex" } },
                                React.createElement("img", { src: item._source.image }),
                                React.createElement(
                                    "div",
                                    { style: { verticalAlign: "top", padding: "8px" } },
                                    item._source.description
                                )
                            )
                        )
                    );
                } else {
                    return React.createElement(
                        "li",
                        { style: { listStyleType: "none", backgroundColor: "white", color: "black" }, id: i },
                        React.createElement(
                            "article",
                            null,
                            React.createElement(
                                "h1",
                                { style: { textAlign: "start" } },
                                React.createElement(
                                    "a",
                                    { target: "_blank", href: that.props.baseUrl + '?id=' + item._id, rel: "external" },
                                    item.title + " " + item.year
                                )
                            ),
                            React.createElement(
                                "div",
                                { style: { display: "flex" } },
                                React.createElement("img", { src: item.image }),
                                React.createElement(
                                    "div",
                                    { style: { verticalAlign: "top", padding: "8px" } },
                                    item.description
                                )
                            )
                        )
                    );
                }
            });
        }
    }]);

    return SearchResults;
}(React.Component);

function renderSearchResults(results, baseUrl) {
    ReactDOM.render(React.createElement(SearchResults, { results: results, baseUrl: baseUrl }), document.getElementById('search-results'));
}