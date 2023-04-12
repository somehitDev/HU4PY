
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
        if (parentId == "hufpy-app-container" || autoAttach) {
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
            if (raw_style == null) {
                return {};
            }
            else {
                var return_style = {};
                for (var style_item of raw_style.slice(0, -1).split(";")) {
                    var split = style_item.split(":");
                    return_style[split[0].trim()] = split[1].trim();
                }

                return return_style;
            }
        }
        else if (name == "width") {
            return `${element.clientWidth}px`;
        }
        else if (name == "height") {
            return `${element.clientHeight}px`;
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
            delete this.$widgets[element.id];
            element.id = value;
            this.$widgets[value] = element;
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
                style_attr += `${key}:${value[key]};`;
            }
            element.setAttribute("style", style_attr);

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
