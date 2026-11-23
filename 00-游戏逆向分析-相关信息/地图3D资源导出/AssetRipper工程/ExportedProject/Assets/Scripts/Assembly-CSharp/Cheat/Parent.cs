namespace Cheat
{
	public class Parent : ChoiceBase
	{
		protected ChoiceBase[] childs;

		public Parent(string name, ChoiceBase[] childs)
			: base(null)
		{
		}

		public override bool OnSelect()
		{
			return false;
		}
	}
}
