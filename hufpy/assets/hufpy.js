
class HufPy {
    constructor() {
        this.$events = {};
        this.$widgets = {
            "hufpy-app-container": document.querySelector("hufpy-app-container")
        };
    }

    addGlobalCss(styleId, styleContent) {
        this.deleteGlobalCss(styleId);

        document.head.insertAdjacentHTML("beforeend", `
<style id="${styleId}">
${styleContent}
</style>
`);
    }

    deleteGlobalCss(styleId) {
        var may_style = document.querySelector(`style#${styleId}`);
        if (may_style != null) {
            may_style.remove();
        }
    }

    createWidget(tagName, widgetClass, widgetType, widgetId, attributes, parentId = "hufpy-app-container", autoAttach = false) {
        // var parent = document.querySelector(`#${parentId}`);
        var parent = null;
        if (parentId.toLowerCase() == "body") {
            parent = document.body;
        }
        else if (parentId == "hufpy-app-container") {
            parent = document.querySelector("#hufpy-app-container");
        }
        else {
            parent = this.$widgets[parentId];
        }

        if (parent == undefined || parent == null) {
            return { state: "fail", message: "unknown parent!" };
        }

        if (widgetType == "widget" && parentId == "hufpy-app-container") {
            return { state: "fail", message: "`Widget` cannot be deployed without `Layout`!" };
        }

        var element = document.createElement(tagName);
        element.className = widgetClass;
        element.id = widgetId;
        for (var key in attributes) {
            this.$setWidgetAttribute(element, key, attributes[key]);
        }
        // element.setAttribute("data-visible", "false");

        if (widgetType == "layout" && parentId == "hufpy-app-container") {
            element.style.width = "100%";
            element.style.height = "100%";
        }

        // parent.appendChild(element);
        this.$widgets[widgetId] = element;
        if ([ "body", "hufpy-app-container" ].includes(parentId) || autoAttach) {
            parent.appendChild(element);
        }

        return { state: "success" };
    }

    removeWidget(widgetId) {
        this.$widgets[widgetId].remove();
    }


    // getWidgetChildren(widgetId) {
    //     var childrenIds = [];
    //     for (var child of document.querySelectorAll(`#${widgetId} > .hufpy-widget`)) {
    //         childrenIds.push(child.id);
    //     }

    //     return childrenIds;
    // }

    getWidgetAttribute(widgetId, attributeName) {
        // return this.$getWidgetAttribute(document.querySelector(`#${widgetId}`), attributeName);
        return this.$getWidgetAttribute(this.$widgets[widgetId], attributeName);
    }

    $getWidgetAttribute(element, name) {
        if (name == "text") {
            return element.innerText;
        }
        else if (name == "value") {
            return element.value;
        }
        else if (name == "checked") {
            return element.checked;
        }
        else if (name == "style") {
            var raw_style = element.getAttribute("style");
            var return_style = {};
            if (![ "", null ].includes(raw_style)) {
                for (var style_item of raw_style.slice(0, -1).split(";")) {
                    var split = style_item.split(":");
                    if (![ "border", "margin", "padding" ].includes(split[0].trim())) {
                        return_style[split[0].trim()] = split[1].trim();
                    }
                }
            }

            if (return_style["width"] == undefined && element.clientWidth != 0) {
                return_style["width"] = `${element.clientWidth}px`;
            }
            if (return_style["height"] == undefined && element.clientHeight != 0) {
                return_style["height"] = `${element.clientHeight}px`
            }

            return_style["border"] = {
                "width": element.style.borderWidth == "" ? "" : parseInt(element.style.borderWidth.slice(0, -2)),
                "style": element.style.borderStyle,
                "color": element.style.borderColor,
                "radius": element.style.borderRadius == "" ? "" : parseInt(element.style.borderRadius.slice(0, -2))
            }
            return_style["margin"] = {
                left: element.style.marginLeft == "" ? "" : parseInt(element.style.marginLeft.slice(0, -2)),
                right: element.style.marginRight == "" ? "" : parseInt(element.style.marginRight.slice(0, -2)),
                top: element.style.marginTop == "" ? "" : parseInt(element.style.marginTop.slice(0, -2)),
                bottom: element.style.marginBottom == "" ? "" : parseInt(element.style.marginBottom.slice(0, -2))
            };
            return_style["padding"] = {
                left: element.style.paddingLeft == "" ? "" : parseInt(element.style.paddingLeft.slice(0, -2)),
                right: element.style.paddingRight == "" ? "" : parseInt(element.style.paddingRight.slice(0, -2)),
                top: element.style.paddingTop == "" ? "" : parseInt(element.style.paddingTop.slice(0, -2)),
                bottom: element.style.paddingBottom == "" ? "" : parseInt(element.style.paddingBottom.slice(0, -2))
            };

            return return_style;
        }
        else {
            return element.getAttribute(name);
        }
    }

    setWidgetAttribute(widgetId, attributeName, attributeValue) {
        // this.$setWidgetAttribute(document.querySelector(`#${widgetId}`), attributeName, attributeValue);
        this.$setWidgetAttribute(this.$widgets[widgetId], attributeName, attributeValue);
    }

    $setWidgetAttribute(element, name, value) {
        if (name == "id") {
            var globalStyle = document.querySelector(`#style_${element.id}`);

            delete this.$widgets[element.id];
            var exist_events = this.$events[element.id];

            element.id = value;

            this.$widgets[value] = element;
            if (exist_events != null) {
                this.$events[value] = exist_events;
            }

            if (globalStyle != null) {
                globalStyle.id = `style_${value}`
            }
        }
        else if (name == "text") {
            element.innerText = value;
        }
        else if (name == "value") {
            element.value = value;
        }
        else if (name == "checked") {
            element.checked = value;
        }
        else if (name == "style") {
            var style_attr = "";
            for (var key in value) {
                if (![ "border", "margin", "padding" ].includes(key)) {
                    style_attr += `${key}:${value[key]};`;
                }
                // if (key == "border") {
                //     element.style.borderWidth = `${value[key]["width"]}px`;
                //     element.style.borderStyle = value[key]["style"];
                //     element.style.borderColor = value[key]["color"];
                //     element.style.borderRadius = `${value[key]["radius"]}px`;
                // }
                // else if (key == "margin") {
                //     element.style.marginLeft = `${value[key]["left"]}px`;
                //     element.style.marginRight = `${value[key]["right"]}px`;
                //     element.style.marginTop = `${value[key]["top"]}px`;
                //     element.style.marginBottom = `${value[key]["bottom"]}px`;
                // }
                // else if (key == "padding") {
                //     element.style.paddingLeft = `${value[key]["left"]}px`;
                //     element.style.paddingRight = `${value[key]["right"]}px`;
                //     element.style.paddingTop = `${value[key]["top"]}px`;
                //     element.style.paddingBottom = `${value[key]["bottom"]}px`;
                // }
            }
            element.setAttribute("style", style_attr);

            // if (value["width"] != undefined) {
            //     element.style.width = value["width"];
            // }
            // if (value["height"] != undefined) {
            //     element.style.height = value["height"];
            // }

            element.style.borderWidth = `${value["border"]["width"]}px`;
            element.style.borderStyle = value["border"]["style"];
            element.style.borderColor = value["border"]["color"];
            element.style.borderRadius = `${value["border"]["radius"]}px`;

            element.style.marginLeft = `${value["margin"]["left"]}px`;
            element.style.marginRight = `${value["margin"]["right"]}px`;
            element.style.marginTop = `${value["margin"]["top"]}px`;
            element.style.marginBottom = `${value["margin"]["bottom"]}px`;

            element.style.paddingLeft = `${value["padding"]["left"]}px`;
            element.style.paddingRight = `${value["padding"]["right"]}px`;
            element.style.paddingTop = `${value["padding"]["top"]}px`;
            element.style.paddingBottom = `${value["padding"]["bottom"]}px`;

            // for (var key in value) {
            //     element.style[key] = value;
            // }
        }
        else {
            element.setAttribute(name, value);
        }
    }

    removeWidgetAttribute(widgetId, attributeName) {
        // this.$removeWidgetAttribute(document.querySelector(`#${widgetId}`), attributeName);
        this.$removeWidgetAttribute(this.$widgets[widgetId], attributeName);
    }

    $removeWidgetAttribute(element, name) {
        element.removeAttribute(name);
    }

    widgetAttributeExsits(widgetId, attributeName) {
        // return this.$widgetAttributeExists(document.querySelector(`#${widgetId}`), attributeName);
        return this.$widgetAttributeExists(this.$widgets[widgetId], attributeName);
    }

    $widgetAttributeExists(element, name) {
        return element.hasAttribute(name);
    }


    $detatchWidget(widgetId, parentId) {
        // var element = document.querySelector(`#${widgetId}`);
        var element = this.$widgets[widgetId];
        var parent = this.$widgets[parentId];

        element.setAttribute("data-visible", "false");
        // document.querySelector(`#${parentId}`).removeChild(element);

        if (parent != undefined) {
            try {
                parent.removeChild(element);
            }
            catch {}
        }

        // document.body.appendChild(element);
    }

    $attachWidget(widgetId, parentId, widgetIdx = null) {
        // var parent = document.querySelector(`#${parentId}`);
        // var element = document.querySelector(`#${widgetId}`);
        var parent = this.$widgets[parentId];
        var element = this.$widgets[widgetId];
        // try {
        //     document.body.removeChild(element);
        // }
        // catch {}

        if (widgetIdx == null) {
            parent.appendChild(element);
        }
        else {
            try {
                parent.insertBefore(parent.children[widgetIdx + 1], element);
            }
            catch {
                parent.appendChild(element);
            }
        }

        element.setAttribute("data-visible", "true");
    }

    setWidgetVisible(widgetId, parentId, visible, widgetIdx = null) {
        if (visible) {
            this.$attachWidget(widgetId, parentId, widgetIdx);
        }
        else {
            this.$detatchWidget(widgetId, parentId);
        }
    }


    bindWidgetEvent(widgetId, eventName, bindName, callArgs = [], callWidgetId = null) {
        if (this.$events[widgetId] != undefined && this.$events[widgetId][eventName] != undefined && this.$events[widgetId][eventName][bindName] != undefined) {
            // document.querySelector(`#${widgetId}`).removeEventListener(eventName, this.$events[widgetId][eventName][bindName]);
            this.$widgets[widgetId].removeEventListener(eventName, this.$events[widgetId][eventName][bindName]);
        }

        var self = this;
        if (this.$events[widgetId] == undefined) {
            this.$events[widgetId] = {};
        }
        if (this.$events[widgetId][eventName] == undefined) {
            this.$events[widgetId][eventName] = {};
        }
        this.$events[widgetId][eventName][bindName] = (ev) => {
            var respArgs = [];
            for (var callArg of callArgs) {
                if (callArg == "self") {
                    respArgs.push(`self.widgets["${widgetId}"]`);
                }
                else if (callArg == "ev" || callArg == "event") {
                    respArgs.push(ev);
                }
                else {
                    respArgs.push(self.$getWidgetAttribute(ev.target, callArg));
                }
            }

            pywebview.api.call_python_widget_event(callWidgetId == null ? widgetId : callWidgetId, bindName, respArgs);
        };
        // document.querySelector(`#${widgetId}`).addEventListener(eventName, this.$events[widgetId][eventName][bindName]);
        this.$widgets[widgetId].addEventListener(eventName, this.$events[widgetId][eventName][bindName]);
    }
};


window.addEventListener("pywebviewready", () => {
    window.hufpy = new HufPy();
});
