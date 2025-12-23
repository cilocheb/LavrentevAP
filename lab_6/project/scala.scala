

object Lab04Complete {


  object BasicScala {
    val square: Int => Int = x => x * x
    val add: (Int, Int) => Int = (a, b) => a + b

    def applyFunction(f: Int => Int, x: Int): Int = f(x)

    def multiply(a: Int)(b: Int): Int = a * b
    val double = multiply(2)

    def factorial(n: Int): Int = {
      if (n <= 1) 1
      else n * factorial(n - 1)
    }

    @annotation.tailrec
    def factorialTailrec(n: Int, acc: Int = 1): Int = {
      if (n <= 1) acc
      else factorialTailrec(n - 1, acc * n)
    }

    def main(args: Array[String]): Unit = {
      println(s"square(5) = ${square(5)}")
      println(s"add(3,4) = ${add(3, 4)}")
      println(s"applyFunction(square, 3) = ${applyFunction(square, 3)}")
      println(s"double(7) = ${double(7)}")
      println(s"factorial(5) = ${factorial(5)}")
      println(s"factorialTailrec(5) = ${factorialTailrec(5)}")
    }
  }


  // 2. COLLECTIONS - MAP, FILTER, REDUCE


  object Collections {
    case class Product(id: Int, name: String, price: Double, category: String, inStock: Boolean)

    val products = List(
      Product(1, "iPhone", 999.99, "electronics", true),
      Product(2, "MacBook", 1999.99, "electronics", false),
      Product(3, "T-shirt", 29.99, "clothing", true),
      Product(4, "Jeans", 79.99, "clothing", true),
      Product(5, "Book", 15.99, "education", false)
    )

    val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    def demonstrateCollections(): Unit = {
      println("\nCOLLECTIONS - MAP/FILTER/REDUCE:")

      // MAP
      val productNames = products.map(_.name)
      println(s"  productNames: $productNames")

      val discountedPrices = products.map(p => p.copy(price = p.price * 0.9))
      println(s"  discountedPrices: ${discountedPrices.map(p => s"${p.name}: $${p.price.toInt}")}")

      // FILTER
      val availableProducts = products.filter(_.inStock)
      println(s"  availableProducts: ${availableProducts.map(_.name)}")

      val expensiveProducts = products.filter(_.price > 100)
      println(s"  expensiveProducts: ${expensiveProducts.map(_.name)}")

      // REDUCE
      val totalPrice = products.map(_.price).reduce(_ + _)
      println(s"  totalPrice: $${totalPrice.toInt}")

      // FOLD
      val totalStockValue = products.foldLeft(0.0)((acc, p) => acc + p.price)
      println(s"  foldLeft totalValue: $${totalStockValue.toInt}")

      // GROUPBY
      val productsByCategory = products.groupBy(_.category)
      println(s"  productsByCategory: ${productsByCategory.keySet}")

      // FOR-COMPREHENSION
      val result = for {
        product <- products
        if product.inStock && product.price < 50
      } yield product.name.toUpperCase()
      println(s"  for-comprehension: $result")

      // CHAINING
      val chainResult = products
        .filter(_.inStock)
        .map(p => (p.name, p.price * 0.8 - 20))
        .sortBy(_._2)
        .take(3)
      println(s"  chainResult: $chainResult")
    }

    def main(args: Array[String]): Unit = {
      demonstrateCollections()
    }
  }

 
  // 3. OPTION & EITHER - ERROR HANDLING


  object ErrorHandling {
    case class User(id: Int, name: String, email: String)
    case class Order(userId: Int, amount: Double, status: String)

    val users = Map(
      1 -> User(1, "John Doe", "john@example.com"),
      2 -> User(2, "Jane Smith", "jane@example.com")
    )

    val orders = List(
      Order(1, 99.99, "completed"),
      Order(2, 149.99, "pending"),
      Order(3, 199.99, "shipped")
    )

    def findUser(id: Int): Option[User] = users.get(id)

    def validateUser(user: User): Either[String, User] = {
      if (user.email.contains("@")) Right(user)
      else Left(s"Invalid email for ${user.name}")
    }

    def processOrder(order: Order): Either[String, (User, Order)] = {
      for {
        user <- findUser(order.userId).toRight(s"User ${order.userId} not found")
        validatedUser <- validateUser(user)
      } yield (validatedUser, order)
    }

    def demonstrateErrorHandling(): Unit = {
      println("\nOPTION & EITHER:")

      val user1 = findUser(1)
      val user3 = findUser(3)
      println(s"  findUser(1): $user1")
      println(s"  findUser(3): $user3")

      user1.foreach(user => println(s"  User name: ${user.name}"))

      val userName = user3.getOrElse(User(0, "Unknown", "")).name
      println(s"  user3 name or default: $userName")

      val userEmail = findUser(1).map(_.email)
      println(s"  Email: $userEmail")

      val validUser = validateUser(User(1, "John", "john@example.com"))
      val invalidUser = validateUser(User(2, "Jane", "invalid-email"))
      println(s"  validUser: $validUser")
      println(s"  invalidUser: $invalidUser")

      val orderResults = orders.map(processOrder)
      orderResults.foreach {
        case Right((user, order)) => println(s"  Order: ${user.name} - $${order.amount}")
        case Left(error) => println(s"  Error: $error")
      }

      val combinedResult = for {
        user1 <- findUser(1).toRight("User 1 not found")
        user2 <- findUser(2).toRight("User 2 not found")
      } yield s"${user1.name} and ${user2.name}"
      println(s"  combinedResult: $combinedResult")
    }

    def main(args: Array[String]): Unit = {
      demonstrateErrorHandling()
    }
  }

 
  // 4. CASE CLASSES & PATTERN MATCHING


  object PatternMatching {
    sealed trait PaymentMethod
    case class CreditCard(number: String, expiry: String) extends PaymentMethod
    case class PayPal(email: String) extends PaymentMethod
    case class Crypto(wallet: String) extends PaymentMethod

    sealed trait OrderStatus
    case object Pending extends OrderStatus
    case object Processing extends OrderStatus
    case class Shipped(trackingNumber: String) extends OrderStatus
    case class Delivered(deliveryDate: String) extends OrderStatus
    case class Cancelled(reason: String) extends OrderStatus

    case class Order(id: Int, amount: Double, payment: PaymentMethod, status: OrderStatus)

    def processPayment(payment: PaymentMethod): String = payment match {
      case CreditCard(number, expiry) => s"${number.reverse.take(4).reverse} / $expiry"
      case PayPal(email) => s"PayPal: $email"
      case Crypto(wallet) => s"Crypto: ${wallet.take(10)}..."
    }

    def canCancelOrder(status: OrderStatus): Boolean = status match {
      case Pending | Processing => true
      case Shipped(_) | Delivered(_) | Cancelled(_) => false
    }

    def updateOrderStatus(order: Order, newStatus: OrderStatus): Order = {
      order.copy(status = newStatus)
    }

    def demonstratePatternMatching(): Unit = {
      println("\nPATTERN MATCHING:")

      val orders = List(
        Order(1, 99.99, CreditCard("1234567812345678", "12/25"), Pending),
        Order(2, 149.99, PayPal("user@example.com"), Processing),
        Order(3, 199.99, Crypto("1A2b3C4d5E6f7G8h9I0j"), Shipped("TRACK123")),
        Order(4, 79.99, CreditCard("8765432187654321", "06/24"), Delivered("2024-01-15"))
      )

      orders.foreach { order =>
        val paymentInfo = processPayment(order.payment)
        val cancelable = if (canCancelOrder(order.status)) "Yes" else "No"
        println(s"  Order ${order.id}: $paymentInfo - Cancelable: $cancelable")
      }

      val pendingCreditCardOrders = for {
        order <- orders
        if order.payment.isInstanceOf[CreditCard]
        if canCancelOrder(order.status)
      } yield order.id
      println(s"  Pending credit card orders: $pendingCreditCardOrders")

      val statusDescriptions = orders.map {
        case Order(id, _, _, Shipped(tracking)) => s"Order $id: Shipped ($tracking)"
        case Order(id, _, _, Delivered(date)) => s"Order $id: Delivered ($date)"
        case Order(id, _, _, status) => s"Order $id: $status"
      }
      statusDescriptions.foreach(println)
    }

    def main(args: Array[String]): Unit = {
      demonstratePatternMatching()
    }
  }


  // 5. PRACTICAL TASKS


  def analyzeSales(products: List[Collections.Product]): Map[String, (Double, Int)] = {
    products
      .filter(_.inStock)
      .groupBy(_.category)
      .map { case (category, prods) => 
        category -> (prods.map(_.price).sum, prods.length) 
      }
      .toMap
  }

  def processOrderPipeline(order: ErrorHandling.Order): Either[String, Double] = {
    for {
      user <- ErrorHandling.findUser(order.userId).toRight("User not found")
      validatedUser <- ErrorHandling.validateUser(user)
      discount = if (order.amount > 100) 0.1 else 0.0
    } yield order.amount * (1 - discount)
  }

  def getOrderSummary(order: PatternMatching.Order): String = order.status match {
    case PatternMatching.Pending => s"Order ${order.id}: waiting for payment"
    case PatternMatching.Processing => s"Order ${order.id}: processing"
    case PatternMatching.Shipped(track) => s"Order ${order.id}: shipped ($track)"
    case PatternMatching.Delivered(date) => s"Order ${order.id}: delivered on $date"
    case PatternMatching.Cancelled(reason) => s"Order ${order.id}: cancelled ($reason)"
  }


  // MAIN


  def main(args: Array[String]): Unit = {
    println("LABORATORY WORK #6: SCALA AND BIG DATA")

    println("\n1. BASIC SCALA:")
    BasicScala.main(Array())

    println("\n2. COLLECTIONS:")
    Collections.main(Array())

    println("\n3. ERROR HANDLING:")
    ErrorHandling.main(Array())

    println("\n4. PATTERN MATCHING:")
    PatternMatching.main(Array())

    println("\n5. PRACTICAL TASKS:")
    
    println("  Task 1 - analyzeSales:")
    val analysis = analyzeSales(Collections.products)
    analysis.foreach { case (cat, (sum, count)) => println(s"    $cat: $${sum.toInt} ($count items)") }

    println("  Task 2 - processOrderPipeline:")
    val order1 = ErrorHandling.Order(1, 150.0, "completed")
    val order2 = ErrorHandling.Order(3, 200.0, "pending")
    println(s"    Order 1: ${processOrderPipeline(order1)}")
    println(s"    Order 2: ${processOrderPipeline(order2)}")

    println("  Task 3 - getOrderSummary:")
    val scalaOrders = List(
      PatternMatching.Order(1, 99.99, PatternMatching.CreditCard("1234", "12/25"), PatternMatching.Pending),
      PatternMatching.Order(2, 149.99, PatternMatching.PayPal("test@test.com"), PatternMatching.Shipped("ABC123")),
      PatternMatching.Order(3, 199.99, PatternMatching.Crypto("wallet123"), PatternMatching.Delivered("2024-01-15"))
    )
    scalaOrders.foreach(order => println(s"    ${getOrderSummary(order)}"))


  }
}
