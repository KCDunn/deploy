using System;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

 
namespace Portfolio.Controllers
{
    public class PortfolioController : Controller
    {
        [HttpGet]
        [Route("")]
        public IActionResult index()
        {
            return View();
        }

        [HttpGet]
        [Route("projects")]
        public IActionResult projects()
        {
            return View();
        }

        [HttpGet]
        [Route("contact")]
        public IActionResult contact()
        {
            return View();
        }

        
        [Route("portfolioForm")]
        [HttpPost]
        public IActionResult PortfolioForm(string name, string email)
        {
            Console.WriteLine("Hello " + name);
            Console.WriteLine("Your Email is " + email);
            // ViewBag.Name = "name";
            // ViewBag.Email = "email";
            return RedirectToAction("contact");
        }
    }
}
