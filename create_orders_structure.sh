#!/bin/bash

# One-liner to create the file structure for the orders app in a Django project.
# mkdir -p file_structure/orders/{logic/{ports,strategies},plugs/{printer,shopify},tests,views} && touch file_structure/orders/{__init__.py,admin.py,apps.py,models.py,serializers.py,urls.py} file_structure/orders/logic/{__init__.py,generate_label.py,run_label_job.py} file_structure/orders/logic/ports/{__init__.py,label_printer.py,order_finder.py,print_settings_finder.py} file_structure/orders/logic/strategies/{__init__.py,auto_selector.py,base_selector.py,manual_selector.py} file_structure/orders/plugs/{__init__.py,settings_provider.py} file_structure/orders/plugs/printer/{__init__.py,console.py,zebra_label_printer.py} file_structure/orders/plugs/shopify/{__init__.py,adapter.py,shopify_fetcher.py,translator.py} file_structure/orders/tests/{__init__.py,test_auto_selector.py,test_manual_selector.py,test_run_label_job.py} file_structure/orders/views/{__init__.py,manual.py,webhook.py}


# Create the orders file structure
mkdir -p file_structure/orders/{logic/{ports,strategies},plugs/{printer,shopify},tests,views}

# Create all the Python files
touch file_structure/orders/__init__.py
touch file_structure/orders/admin.py
touch file_structure/orders/apps.py
touch file_structure/orders/models.py
touch file_structure/orders/serializers.py
touch file_structure/orders/urls.py

# Logic folder files
touch file_structure/orders/logic/__init__.py
touch file_structure/orders/logic/generate_label.py
touch file_structure/orders/logic/run_label_job.py

# Logic/ports folder files
touch file_structure/orders/logic/ports/__init__.py
touch file_structure/orders/logic/ports/label_printer.py
touch file_structure/orders/logic/ports/order_finder.py
touch file_structure/orders/logic/ports/print_settings_finder.py

# Logic/strategies folder files
touch file_structure/orders/logic/strategies/__init__.py
touch file_structure/orders/logic/strategies/auto_selector.py
touch file_structure/orders/logic/strategies/base_selector.py
touch file_structure/orders/logic/strategies/manual_selector.py

# Plugs folder files
touch file_structure/orders/plugs/__init__.py
touch file_structure/orders/plugs/settings_provider.py

# Plugs/printer folder files
touch file_structure/orders/plugs/printer/__init__.py
touch file_structure/orders/plugs/printer/console.py
touch file_structure/orders/plugs/printer/zebra_label_printer.py

# Plugs/shopify folder files
touch file_structure/orders/plugs/shopify/__init__.py
touch file_structure/orders/plugs/shopify/adapter.py
touch file_structure/orders/plugs/shopify/shopify_fetcher.py
touch file_structure/orders/plugs/shopify/translator.py

# Tests folder files
touch file_structure/orders/tests/__init__.py
touch file_structure/orders/tests/test_auto_selector.py
touch file_structure/orders/tests/test_manual_selector.py
touch file_structure/orders/tests/test_run_label_job.py

# Views folder files
touch file_structure/orders/views/__init__.py
touch file_structure/orders/views/manual.py
touch file_structure/orders/views/webhook.py

echo 
echo "Orders file structure created successfully!"
