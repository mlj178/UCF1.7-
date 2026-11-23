namespace Cheat
{
	public abstract class ChoiceBase
	{
		public Parent parent;

		public int index;

		protected string name;

		public ChoiceBase(string name)
		{
		}

		public abstract bool OnSelect();

		public virtual string GetText()
		{
			return null;
		}

		public virtual bool GetFocus()
		{
			return false;
		}
	}
}
