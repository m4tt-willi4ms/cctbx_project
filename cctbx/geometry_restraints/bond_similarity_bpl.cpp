#include <cctbx/boost_python/flex_fwd.h>

#include <boost/python/def.hpp>
#include <boost/python/class.hpp>
#include <boost/python/args.hpp>
#include <boost/python/return_value_policy.hpp>
#include <boost/python/copy_const_reference.hpp>
#include <boost/python/return_by_value.hpp>
#include <scitbx/array_family/boost_python/shared_wrapper.h>
#include <scitbx/array_family/selections.h>
#include <scitbx/stl/map_wrapper.h>
#include <cctbx/geometry_restraints/bond_similarity.h>

namespace cctbx { namespace geometry_restraints {
namespace {

  struct bond_similarity_proxy_wrappers : boost::python::pickle_suite
  {
    typedef bond_similarity_proxy w_t;

    static boost::python::tuple
      getinitargs(w_t const& self)
    {
      return boost::python::make_tuple(self.i_seqs,
        self.sym_ops,
        self.weights);
    }

    static void
    wrap()
    {
      using namespace boost::python;
      typedef return_value_policy<return_by_value> rbv;
      class_<w_t>("bond_similarity_proxy", no_init)
        .def(init<
          af::shared<af::tiny<std::size_t, 2> >,
          af::shared<double> const&>((
            arg("i_seqs"),
            arg("weights"))))
        .def(init<
          af::shared<af::tiny<std::size_t, 2> >,
          af::shared<sgtbx::rt_mx>,
          af::shared<double> const&>((
            arg("i_seqs"),
            arg("sym_ops"),
            arg("weights"))))
        .add_property("i_seqs", make_getter(&w_t::i_seqs, rbv()))
        .add_property("weights", make_getter(&w_t::weights, rbv()))
        .add_property("sym_ops", make_getter(&w_t::sym_ops, rbv()))
        .def_pickle(bond_similarity_proxy_wrappers())
        ;
      {
        typedef return_internal_reference<> rir;
        scitbx::af::boost_python::shared_wrapper<
          bond_similarity_proxy, rir>::wrap(
          "shared_bond_similarity_proxy");
      }
    }
  };

  struct bond_similarity_wrappers : boost::python::pickle_suite
  {
    typedef bond_similarity w_t;

    static boost::python::tuple
      getinitargs(w_t const& self)
    {
      return boost::python::make_tuple(self.sites_array,
        self.weights);
    }

    static void
    wrap()
    {
      using namespace boost::python;
      typedef return_value_policy<copy_const_reference> ccr;
      typedef return_value_policy<return_by_value> rbv;
      scitbx::af::boost_python::shared_wrapper<
        af::tiny<scitbx::vec3<double>, 2>, rbv>::wrap(
        "sites_array");
      class_<w_t>("bond_similarity", no_init)
        .def(init<
          af::shared<af::tiny<scitbx::vec3<double>, 2> > const&,
          af::shared<double> const&>((
            arg("sites_array"),
            arg("weights"))))
        .def(init<uctbx::unit_cell const&,
                  af::const_ref<scitbx::vec3<double> > const&,
                  bond_similarity_proxy const&>(
          (arg("unit_cell"), arg("sites_cart"), arg("proxy"))))
        .def(init<af::const_ref<scitbx::vec3<double> > const&,
                  bond_similarity_proxy const&>(
          (arg("sites_cart"), arg("proxy"))))
        .add_property("sites_array", make_getter(
          &w_t::sites_array, rbv()))
        .add_property("weights", make_getter(&w_t::weights, rbv()))
        .def("deltas", &w_t::deltas, ccr())
        .def("rms_deltas", &w_t::rms_deltas)
        .def("residual", &w_t::residual)
        .def("gradients", &w_t::gradients)
        .def("mean_distance", &w_t::mean_distance)
        .def_pickle(bond_similarity_wrappers())
        ;
    }
  };

  void
  wrap_all()
  {
    using namespace boost::python;
    bond_similarity_proxy_wrappers::wrap();
    bond_similarity_wrappers::wrap();
    def("bond_similarity_deltas_rms",
      (af::shared<double>(*)(
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&))
      bond_similarity_deltas_rms,
      (arg("sites_cart"), arg("proxies")));
    def("bond_similarity_residuals",
      (af::shared<double>(*)(
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&))
      bond_similarity_residuals,
      (arg("sites_cart"), arg("proxies")));
    def("bond_similarity_residual_sum",
      (double(*)(
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&,
        af::ref<scitbx::vec3<double> > const&))
      bond_similarity_residual_sum,
      (arg("sites_cart"),
       arg("proxies"),
       arg("gradient_array")));
    def("bond_similarity_deltas_rms",
      (af::shared<double>(*)(
        uctbx::unit_cell const&,
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&))
      bond_similarity_deltas_rms,
      (arg("unit_cell"), arg("sites_cart"), arg("proxies")));
    def("bond_similarity_residuals",
      (af::shared<double>(*)(
        uctbx::unit_cell const&,
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&))
      bond_similarity_residuals,
      (arg("unit_cell"), arg("sites_cart"), arg("proxies")));
    def("bond_similarity_residual_sum",
      (double(*)(
        uctbx::unit_cell const&,
        af::const_ref<scitbx::vec3<double> > const&,
        af::const_ref<bond_similarity_proxy> const&,
        af::ref<scitbx::vec3<double> > const&))
      bond_similarity_residual_sum,
      (arg("unit_cell"),
       arg("sites_cart"),
       arg("proxies"),
       arg("gradient_array")));
  }

} // namespace <anonymous>

namespace boost_python {

  void
  wrap_bond_similarity() { wrap_all(); }

}}} // namespace cctbx::geometry_restraints::boost_python
